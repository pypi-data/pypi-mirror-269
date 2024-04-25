import os
import typing as T
import time
import orjson
import asyncio
import logging
import sentry_sdk
from sqlalchemy import text, RowMapping, Engine, create_engine, CursorResult
from sqlalchemy.exc import (
    OperationalError,
    ResourceClosedError,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy import log as sqlalchemy_log

logger = logging.getLogger("SQLAlchemyEngine")


sqlalchemy_log._add_default_handler = lambda x: None  # Patch to avoid duplicate logging


class SQLError(Exception):
    pass


class NoRowsReturnedError(SQLError):
    pass


class TooManyRowsReturnedError(SQLError):
    pass


def build_engine(echo: bool) -> AsyncEngine:
    dsn = os.environ["POSTGRES_DSN"].replace("sql://", "sql+asyncpg://")
    return create_async_engine(
        dsn, echo=echo, echo_pool=echo, pool_size=50, future=True, pool_recycle=300
    )


def build_sync_engine(echo: bool) -> Engine:
    dsn = os.environ["POSTGRES_DSN"].replace("sql://", "sql+psycopg://")
    return create_engine(
        dsn, echo=echo, echo_pool=echo, pool_size=50, future=True, pool_recycle=300
    )


SHOULD_ECHO: bool = True

ENGINE: AsyncEngine = build_engine(echo=SHOULD_ECHO)
# SYNC_ENGINE: Engine = build_sync_engine(echo=SHOULD_ECHO)


def replace_engine() -> None:
    global ENGINE
    logger.debug("[replace engine] closing engine")
    ENGINE = build_engine(echo=SHOULD_ECHO)
    logger.debug("[replace engine] replaced engine")


class SQLPool:
    @property
    def engine(self) -> AsyncEngine:
        return ENGINE

    @staticmethod
    def map_and_fetch(
        only_one: bool, confirm_only_one: bool, execution_res: CursorResult
    ) -> T.Sequence[RowMapping] | RowMapping | str | None:
        if only_one:
            with sentry_sdk.start_span(description="fetchone"):
                res = execution_res.mappings().fetchone()
        else:
            with sentry_sdk.start_span(description="fetchall"):
                res = execution_res.mappings().fetchall()
            if confirm_only_one:
                res = SQLPool.validate_one_record(records=res)
        return res

    @staticmethod
    def validate_one_record(records: T.Sequence[RowMapping]) -> RowMapping:
        raw_vals_len = len(records)
        if raw_vals_len == 0:
            raise NoRowsReturnedError("No rows updated.")
        if raw_vals_len > 1:
            raise TooManyRowsReturnedError(
                f"More than one row ({raw_vals_len}) was returned for this patch, so rolled back."
            )
        return records[0]

    async def _query(
        self,
        query: str,
        only_one: bool,
        /,
        *args,
        log_query: bool,
        conn: AsyncConnection | None = None,
        times: int = 0,
        confirm_only_one: bool = False,
        **kwargs,
    ) -> T.Sequence[RowMapping] | RowMapping | str | None:
        """Confirming only one waits until the results are verified to be only one before committing.
        Otherwise, results are default automatically committed"""
        if only_one and confirm_only_one:
            raise SQLError(
                "You cannot give only_one=True and confirm_only_one=True. Give one or the other."
            )
        with sentry_sdk.start_span(description="query_sqlalchemy"):
            start_time = time.time()
            inside_conn = time.time()
            try:
                if conn:
                    with sentry_sdk.start_span(description="execute"):
                        execution_res = await conn.execute(text(query), *args, **kwargs)
                    row_res = self.map_and_fetch(
                        only_one=only_one,
                        execution_res=execution_res,
                        confirm_only_one=confirm_only_one,
                    )
                else:
                    async with self.engine.connect() as _conn:
                        if not confirm_only_one:
                            await _conn.execution_options(isolation_level="AUTOCOMMIT")
                        with sentry_sdk.start_span(description="execute"):
                            execution_res = await _conn.execute(
                                text(query), *args, **kwargs
                            )
                        row_res = self.map_and_fetch(
                            only_one=only_one,
                            execution_res=execution_res,
                            confirm_only_one=confirm_only_one,
                        )
                        if confirm_only_one:
                            await _conn.commit()
                inner_end = time.time()
            except (OperationalError, ResourceClosedError) as e:
                logger.error(f"{e=}, {times=}")
                sentry_sdk.capture_exception(e)
                if times < 5:
                    replace_engine()
                    await asyncio.sleep(5)
                    res = await self._query(
                        query,
                        only_one,
                        *args,
                        log_query=log_query,
                        times=times + 1,
                        **kwargs,
                    )
                    logger.error(
                        f"Result after replacing pool worked! {str(res)[0:10]}"
                    )
                    return res
                else:
                    logger.debug(f"OPERATION ERROR TOO MANY TIMES: {times=}")
                    raise e
            except Exception as e:
                logger.debug(f"[ERROR Query]\n{query}\n[ERROR]{e}")
                raise e
            outside_end = time.time()
            conn_took_ms = round((inside_conn - start_time) * 1_000, 2)
            inner_took_ms = round((inner_end - start_time) * 1_000, 2)
            outside_took_ms = round((outside_end - inner_end) * 1_000, 2)
            took_str = f"*[SQLALCHEMY Query Took] {inner_took_ms} ms, acquiring con: {conn_took_ms} ms, returning con: {outside_took_ms}*"
            if log_query:
                took_str = f"[Query]\n{query}\n\n{took_str}"
            logger.debug(took_str)
            return row_res

    async def query_records(
        self,
        query: str,
        *args,
        log_query: bool = True,
        conn: AsyncConnection | None = None,
        confirm_only_one: bool = False,
        **kwargs,
    ) -> list[RowMapping] | None:
        return await self._query(
            query,
            False,
            *args,
            log_query=log_query,
            conn=conn,
            confirm_only_one=confirm_only_one,
            **kwargs,
        )

    async def query_record(
        self,
        query: str,
        *args,
        log_query: bool = True,
        conn: AsyncConnection | None = None,
        **kwargs,
    ) -> RowMapping | str | None:
        return await self._query(
            query, True, *args, log_query=log_query, conn=conn, **kwargs
        )

    async def query_val(
        self,
        query: str,
        *args,
        log_query: bool = True,
        conn: AsyncConnection | None = None,
        **kwargs,
    ) -> T.Any:
        record = await self.query_record(
            query, *args, log_query=log_query, conn=conn, **kwargs
        )
        if record is None:
            return None
        return next(iter(record.values()))

    async def query_json(
        self,
        query: str,
        *args,
        log_query: bool = True,
        conn: AsyncConnection | None = None,
        **kwargs,
    ) -> dict[str, T.Any] | list[dict[str, T.Any]] | None:
        res = await self.query_record(
            query, *args, log_query=log_query, conn=conn, **kwargs
        )
        if res is None:
            return None
        return orjson.loads(res)

    async def query_single_json(
        self,
        query: str,
        *args,
        log_query: bool = True,
        conn: AsyncConnection | None = None,
        **kwargs,
    ) -> dict[str, T.Any] | None:
        j = await self.query_json(
            query, *args, log_query=log_query, conn=conn, **kwargs
        )
        if isinstance(j, list):
            if len(j) == 1:
                return j[0]
            if len(j) == 0:
                return None
            if len(j) > 1:
                raise SQLError(f"Expected only one value, got {len(j)}.")
        return j


sql_pool = SQLPool()
