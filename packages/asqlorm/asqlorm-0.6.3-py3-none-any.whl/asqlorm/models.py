import typing as T
import json
import logging
from enum import Enum
from pydantic import BaseModel, PrivateAttr, model_validator, TypeAdapter
from pydantic_core import PydanticUndefined

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import RowMapping

from fastgql.query_builders.sql.query_builder import QueryBuilder, Cardinality

from asqlorm.sql.sql_alchemy import sql_pool, NoRowsReturnedError
from asqlorm.utils import TYPES_MAP

logger = logging.getLogger(__name__)


class raw_sql(BaseModel):
    stmt: str
    variables: dict[str, T.Any] | None = None


class FilterConnector(str, Enum):
    AND = " AND "
    OR = " OR "


class UpdateOperation(str, Enum):
    REPLACE = ":="
    ADD = "+="
    REMOVE = "-="


class UnsetError(Exception):
    pass


class ResolverError(Exception):
    pass


class NodeError(Exception):
    pass


VARS = dict[str, T.Any]
CONVERSION_FUNC = T.Callable[[str], T.Any]


IGNORE_SET: set[str] = {
    "__pydantic_validator__",
    "model_fields_set",
    "model_fields",
    "__pydantic_fields_set__",
}


class ConflictAction(str, Enum):
    DO_UPDATE = "DO UPDATE"
    DO_NOTHING = "DO NOTHING"


class Edge(BaseModel):
    from_: str
    cardinality: Cardinality
    is_required: bool


class EdgeWithResolver(Edge):
    resolver_type: T.Type["ResolverType"] | str


class ChildEdge(Edge):
    resolver: "ResolverType"


class ComputedColumn(BaseModel):
    path: str
    data_type: str = None
    is_nullable: bool

    basemodel_type: T.Type[BaseModel] | None = None
    cardinality: Cardinality = Cardinality.ONE

    custom_converter: T.Callable = None

    override: bool = None

    include_args_annotation: str = None
    update_qb: T.Callable[[QueryBuilder, T.Any], None] = None

    @model_validator(mode="after")
    def validate_column(self) -> "ComputedColumn":
        if not self.data_type and not self.custom_converter:
            raise ValueError(
                "You must provide either a data_type or a custom_converter."
            )
        if self.data_type and self.custom_converter:
            raise ValueError(
                "You cannot provide both a data_type or a custom_converter."
            )
        return self

    def __hash__(self):
        return hash(self.path)


class ComputedLink(BaseModel):
    node_name: str
    cardinality: Cardinality = Cardinality.ONE
    is_nullable: bool
    from_: str
    # from mapping for inheritance, like GiphyImage vs CloudinaryImage
    from_mapping: dict[str, str] | None = None

    annotations_by_kwarg: dict[str, str] = None
    update_qb: T.Callable[[QueryBuilder, T.Any], None] = None


class Node(BaseModel):
    def __getattribute__(self, name: str):
        if name not in IGNORE_SET and name not in self.model_fields_set:
            if name in self.model_fields:
                raise UnsetError(f"{name} is unset.")
        return super().__getattribute__(name)

    _children_cache: dict[str, "NodeType"] = PrivateAttr(default_factory=dict)

    _resolver_used: T.Optional["Resolver"] = PrivateAttr(None)

    __edges_map__: T.ClassVar[dict[str, EdgeWithResolver]]

    __computed_columns__: T.ClassVar[dict[str, ComputedColumn]]
    __computed_links__: T.ClassVar[dict[str, ComputedLink]]
    __table_name__: T.ClassVar[str]
    __primary_keys__: T.ClassVar[list[str]]

    _computed: dict[str, T.Any] = PrivateAttr(default_factory=dict)

    __columns_in_order__: T.ClassVar[list[str]]

    @property
    def computed(self) -> dict[str, T.Any]:
        return self._computed

    def _resolve_node(self, key: str) -> T.Union["NodeType", list["NodeType"]]:
        if key not in self._children_cache:
            raise NodeError(f"{key} is unset.")
        return self._children_cache[key]


NodeType = T.TypeVar("NodeType", bound=Node)


class Insert(BaseModel):
    pass


class Patch(BaseModel):
    pass


class Conflict(BaseModel):
    unique_index_str: str
    action: ConflictAction
    patch: T.Optional[Patch] = None
    columns_to_upsert: list[str] | None = None
    return_conflicting_rows: bool

    @model_validator(mode="after")
    def validate_action(self) -> "Conflict":
        if self.action == ConflictAction.DO_NOTHING and (
            self.patch or self.columns_to_upsert
        ):
            raise ValueError(
                "If the action is DO_NOTHING, do not give a patch or columns to upsert."
            )
        if self.action == ConflictAction.DO_UPDATE and not (
            self.patch or self.columns_to_upsert
        ):
            raise ValueError(
                "You must provide a patch or columns to upsert when the action is DO_UPDATE."
            )
        if (
            self.action == ConflictAction.DO_UPDATE
            and self.return_conflicting_rows is False
        ):
            raise ValueError(
                "If DO_UPDATE then it will always return conflicting rows, so return_conflicting_rows cannot be False."
            )
        return self

    def unique_column_names(self) -> list[str]:
        return [
            c_name.replace("(", "").replace(")", "").strip()
            for c_name in self.unique_index_str.split(",")
        ]


InsertType = T.TypeVar("InsertType", bound=Insert)


class Resolver(BaseModel):
    def __init__(self, /, **data: T.Any) -> None:  # type: ignore
        super().__init__(**data)
        self._qb = QueryBuilder(
            table_name=f'"{self._node.__table_name__}"',
            cardinality=Cardinality.ONE,  # This is dummy, change at build step
            from_=None,
        )
        for primary_key in self._node.__primary_keys__:
            self._qb.sel(name=primary_key, path=f"$current.{primary_key}")

    _node: T.ClassVar[T.Type[NodeType]]

    _qb: QueryBuilder = PrivateAttr

    _children: dict[str, "ChildEdge"] = PrivateAttr(default_factory=dict)

    _runtime__computed_columns__: dict[str, ComputedColumn] = PrivateAttr(
        default_factory=dict
    )

    def to_qb(
        self, cardinality: Cardinality, from_: str | None, replace_from: bool = True
    ) -> QueryBuilder:
        self._qb.cardinality = cardinality
        self._qb.set_from(from_=from_, replace_from=replace_from)
        return self._qb

    def build(
        self, cardinality: Cardinality, format_sql: bool = False, is_count: bool = False
    ) -> tuple[str, dict[T.Any]]:
        self._qb.cardinality = cardinality
        return self._qb.build_root(format_sql=format_sql, is_count=is_count)

    def add_query_variables(
        self: "ThisResolverType", variables: VARS | None
    ) -> "ThisResolverType":
        if variables:
            self._qb.add_variables(variables)
        return self

    def and_where(
        self: "ThisResolverType",
        filter_str: str,
        variables: VARS | None = None,
        replace_variables: bool = False,
    ) -> "ThisResolverType":
        self._qb.and_where(
            where=filter_str, variables=variables, replace_variables=replace_variables
        )
        return self

    def set_where(
        self: "ThisResolverType",
        where: str,
        variables: dict[str, T.Any] | None = None,
        replace_where: bool = False,
        replace_variables: bool = False,
    ) -> "ThisResolverType":
        self._qb.set_where(
            where=where,
            variables=variables,
            replace_where=replace_where,
            replace_variables=replace_variables,
        )
        return self

    def filter(
        self: "ThisResolverType", filter_str: str, variables: VARS | None = None
    ) -> "ThisResolverType":
        return self.and_where(filter_str=filter_str, variables=variables)

    def _filter_by(self: "ThisResolverType", **kwargs: T.Any) -> "ThisResolverType":
        kwargs = {k: v for k, v in kwargs.items() if v is not PydanticUndefined}
        if not kwargs:
            raise ResolverError("Nothing to filter by.")
        filter_strs = []
        variables = {}
        for field_name, field_value in kwargs.items():
            if computed_c := self._node.__computed_columns__.get(field_name):
                left_side = computed_c.path
            else:
                left_side = f"$current.{field_name}"
            if field_value is None:
                filter_strs.append(f"{left_side} IS NULL")
            else:
                filter_strs.append(f"{left_side} = ${field_name}")
                variables[field_name] = field_value
        filter_str = " AND ".join(sorted(filter_strs))
        return self.filter(filter_str=filter_str, variables=variables)

    def _filter_in(self: "ThisResolverType", **kwargs: T.Any) -> "ThisResolverType":
        kwargs = {k: v for k, v in kwargs.items() if v is not PydanticUndefined}
        if not kwargs:
            raise ResolverError("Nothing to filter by.")
        filter_strs = []
        variables = {}
        for field_name, value_lst in kwargs.items():
            if computed_c := self._node.__computed_columns__.get(field_name):
                left_side = computed_c.path
            else:
                left_side = f"$current.{field_name}"
            filter_strs.append(f"{left_side} = ANY(${field_name})")
            variables[field_name] = value_lst
        filter_str = " AND ".join(sorted(filter_strs))
        return self.filter(filter_str=filter_str, variables=variables)

    def order_by(
        self: "ThisResolverType", order_by_str: str, variables: VARS | None = None
    ) -> "ThisResolverType":
        self._qb.set_order_by(order_by=order_by_str, variables=variables)
        return self

    def offset(self: "ThisResolverType", /, _: int | None) -> "ThisResolverType":
        self._qb.set_offset(offset=_)
        return self

    def limit(self: "ThisResolverType", /, _: int | None) -> "ThisResolverType":
        self._qb.set_limit(limit=_)
        return self

    def include_fields(
        self: "ThisResolverType", *fields_to_include: str
    ) -> "ThisResolverType":
        for f in fields_to_include:
            if computed_col := self._node.__computed_columns__.get(f):
                self._qb.sel(name=f, path=computed_col.path)
            else:
                self._qb.sel(f)
        return self

    def _include(self: "ThisResolverType", **kwargs) -> "ThisResolverType":
        fields_to_include: list[str] = []
        for k, v in kwargs.items():
            if v is False or v is PydanticUndefined:
                continue
            if v is not True:
                # must be computed update qb
                self._node.__computed_columns__[k].update_qb(self._qb, *v)
            fields_to_include.append(k)
        return self.include_fields(*fields_to_include)

    def include_all_columns(
        self: "ThisResolverType",
        include_computed_columns: bool = False,
        exclude: set[str] | None = None,
        variables: dict[str, T.Any] | None = None,
    ) -> "ThisResolverType":
        cols = self._node.model_fields.keys()
        if not include_computed_columns:
            cols = cols - {
                k for k, v in self._node.__computed_columns__.items() if not v.override
            }
        if exclude:
            cols = cols - exclude
        if variables:
            self.add_query_variables(variables)
        self.include_fields(*cols)
        return self

    def add_child(
        self: "ThisResolverType",
        key: str,
        resolver: "ResolverType",
        cardinality: Cardinality,
        from_: str,
        is_required: bool,
    ) -> "ThisResolverType":
        if key in self._children:
            raise ResolverError(f"Key {key} is already set.")
        child_edge = ChildEdge(
            resolver=resolver,
            cardinality=cardinality,
            from_=from_,
            is_required=is_required,
        )
        self._children[key] = child_edge
        child_qb = child_edge.resolver.to_qb(
            cardinality=child_edge.cardinality, from_=child_edge.from_
        )
        self._qb.sel_sub(key, child_qb)
        return self

    def add_computed(
        self: "ThisResolverType", name: str, computed_column: ComputedColumn
    ) -> "ThisResolverType":
        if name in self._runtime__computed_columns__:
            raise ResolverError(f"Computed column {name} is already given.")
        self._runtime__computed_columns__[name] = computed_column
        self._qb.sel(name=name, path=computed_column.path)
        return self

    def computed(
        self: "ThisResolverType",
        *,
        name: str,
        path: str,
        data_type: str = None,
        is_nullable: bool,
        custom_converter: T.Callable = None,
    ) -> "ThisResolverType":
        if name in self._runtime__computed_columns__:
            raise ResolverError(f"Computed column {name} is already given.")
        computed_kwargs = {
            k: v
            for k, v in {
                "path": path,
                "data_type": data_type,
                "is_nullable": is_nullable,
                "custom_converter": custom_converter,
            }.items()
            if v is not None
        }
        computed_column = ComputedColumn(**computed_kwargs)
        return self.add_computed(name=name, computed_column=computed_column)

    async def _get_node(
        self,
        field_name: str,
        value: T.Any,
        format_sql: bool = False,
        conn: AsyncConnection | None = None,
    ) -> T.Optional[NodeType]:
        if isinstance(value, tuple):
            keys = field_name.split("__")
            if len(keys) != len(value):
                raise ResolverError(
                    f"Keys length: {keys=} does not match tuple length: {value=}"
                )
            left_side_strs: list[str] = []
            right_side_strs: list[str] = []
            variables: dict[str, T.Any] = {}
            for key, val in zip(keys, value):
                left_side_strs.append(f"$current.{key}")
                right_side_strs.append(f"${key}")
                variables[key] = val

            self.filter(
                f"({', '.join(left_side_strs)}) = ({', '.join(right_side_strs)})",
                variables,
            )
        else:
            self._filter_by(**{field_name: value}).limit(1)
        s, v = self.build(cardinality=Cardinality.ONE, format_sql=format_sql)
        raw_val = await sql_pool.query_val(s, v, log_query=False, conn=conn)
        if raw_val is None:
            return None
        return self.parse_node(**raw_val)

    async def _get(
        self, conn: AsyncConnection | None = None, **kwargs
    ) -> T.Optional[NodeType]:
        field_name, value = validate_get_kwargs(**kwargs)
        return await self._get_node(field_name=field_name, value=value, conn=conn)

    async def _gerror(self, conn: AsyncConnection | None = None, **kwargs) -> NodeType:
        field_name, value = validate_get_kwargs(**kwargs)
        node = await self._get_node(field_name=field_name, value=value, conn=conn)
        if not node:
            raise ResolverError(
                f"{self._node.__name__} not found where {field_name} == {value}."
            )
        return node

    async def count(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
    ) -> int:
        s, v = self.build(
            cardinality=Cardinality.MANY, format_sql=format_sql, is_count=True
        )
        return await sql_pool.query_val(s, v, log_query=log_query, conn=conn)

    async def _query(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
    ) -> list[NodeType]:
        s, v = self.build(cardinality=Cardinality.MANY, format_sql=format_sql)
        raw_list = await sql_pool.query_val(s, v, log_query=log_query, conn=conn)
        return [self.parse_node(**item) for item in raw_list]

    async def first_or_none(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
    ) -> T.Optional[NodeType]:
        s, v = self.limit(1).build(cardinality=Cardinality.MANY, format_sql=format_sql)
        raw_list = await sql_pool.query_val(s, v, log_query=log_query, conn=conn)
        if not raw_list:
            return None
        return self.parse_node(**raw_list[0])

    async def first(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
    ) -> NodeType:
        node = await self.first_or_none(
            format_sql=format_sql, log_query=log_query, conn=conn
        )
        if not node:
            raise ResolverError("No value found.")
        return node

    async def one_or_none(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
    ) -> T.Optional[NodeType]:
        s, v = self.limit(2).build(cardinality=Cardinality.MANY, format_sql=format_sql)
        raw_list = await sql_pool.query_val(s, v, log_query=log_query, conn=conn)
        raw_list_len = len(raw_list)
        if raw_list_len == 0:
            return None
        if raw_list_len > 1:
            raise ResolverError("More than one result returned.")
        return self.parse_node(**raw_list[0])

    async def one(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
    ) -> NodeType:
        node = await self.one_or_none(
            format_sql=format_sql, log_query=log_query, conn=conn
        )
        if not node:
            raise ResolverError("No value found.")
        return node

    def parse_mutation_model(
        self, model: Insert | Patch, prefix: str | None = None
    ) -> tuple[dict[str, str], dict[str, T.Any]]:
        # mode json is incorrect for date-times
        dump_d = model.model_dump(mode="python", exclude_unset=True)
        field_names_to_value_strs: dict[str, str] = {}
        variables: dict[str, T.Any] = {}
        for k, dump_v in dump_d.items():
            model_v = getattr(model, k)
            if isinstance(model_v, raw_sql):
                if model_v.variables:
                    for raw_k, raw_v in model_v.variables.items():
                        if raw_k in variables and raw_v != variables[raw_k]:
                            raise ResolverError(
                                f"Variables {raw_k} is already being used."
                            )
                        variables[raw_k] = raw_v
                field_names_to_value_value = model_v.stmt
            else:
                v = dump_v
                if isinstance(v, dict):
                    v = json.dumps(v)
                if computed_c := self._node.__computed_columns__.get(k):
                    if computed_c.basemodel_type:
                        if model_v is not None:
                            if computed_c.cardinality == Cardinality.ONE:
                                v = model_v.model_dump_json()
                            else:
                                v = (
                                    TypeAdapter(list[computed_c.basemodel_type])
                                    .dump_json(model_v)
                                    .decode("utf-8")
                                )
                if prefix:
                    variable_name = f"{prefix}{k}"
                else:
                    variable_name = k
                if variable_name in variables and v != variables[variable_name]:
                    raise ResolverError(
                        f"Variable '{variable_name}' is already being used."
                    )
                variables[variable_name] = v
                field_names_to_value_value = f":{variable_name}"
            field_names_to_value_strs[k] = field_names_to_value_value
        return field_names_to_value_strs, variables

    def build_conflict_str(
        self, conflict: Conflict | None, existing_variables: dict[str, T.Any] | None
    ) -> tuple[str, dict[str, T.Any]]:
        if existing_variables is None:
            existing_variables = {}
        conflict_str = ""
        if conflict:
            conflict_str = (
                f"ON CONFLICT {conflict.unique_index_str} {conflict.action.value}"
            )
            conflict_strs: list[str] = []
            if conflict.patch:
                _field_names_to_value_strs, _variables = self.parse_mutation_model(
                    model=conflict.patch, prefix="_patch_"
                )
                for _k, _v in _variables.items():
                    if _k in existing_variables and _v != existing_variables[_k]:
                        raise ResolverError(
                            f"Conflict variable '{_k}' is already being used."
                        )
                    existing_variables[_k] = _v
                for _field_name, _value in _field_names_to_value_strs.items():
                    conflict_strs.append(f"{_field_name} = {_value}")
            if conflict.columns_to_upsert:
                for col in conflict.columns_to_upsert:
                    conflict_strs.append(f"{col} = excluded.{col}")
            if conflict_strs:
                conflict_str = f'{conflict_str} SET {", ".join(conflict_strs)}'
        return conflict_str, existing_variables

    def build_insert_q_and_v(
        self,
        insert: Insert,
        conflict: Conflict | None = None,
    ) -> tuple[str, dict[str, T.Any]]:
        field_names_to_value_strs, variables = self.parse_mutation_model(model=insert)

        conflict_str, variables = self.build_conflict_str(
            conflict=conflict, existing_variables=variables
        )

        if (
            conflict_str
            and conflict.action == ConflictAction.DO_NOTHING
            and conflict.return_conflicting_rows
        ):
            conflict_col_names = conflict.unique_column_names()
            unique_col_names_strs: list[str] = []
            for n in conflict_col_names:
                if n not in field_names_to_value_strs:
                    raise ResolverError(
                        f"Cannot return conflicting rows on {n} since {n} was not given for the insert."
                    )
                unique_col_names_strs.append(field_names_to_value_strs[n])
            unique_col_names_str = ", ".join(
                [field_names_to_value_strs[c_name] for c_name in conflict_col_names]
            )
            if len(conflict_col_names) > 1:
                unique_col_names_str = f"({unique_col_names_str})"
            where_unique_index_str = conflict.unique_index_str
            if len(conflict_col_names) == 1:
                where_unique_index_str = conflict.unique_index_str.replace(
                    "(", ""
                ).replace(")", "")
            conflicting_from_str = f"{self._table_name} WHERE {where_unique_index_str} = {unique_col_names_str}"
            complex_return_str = self._returning_str_complex(use_table_name=False)
            return_select_str = f"""
, combined AS (
    SELECT {complex_return_str} FROM inserted
    UNION ALL
    SELECT {complex_return_str} FROM {conflicting_from_str}
    AND NOT EXISTS (SELECT 1 FROM inserted)
)
SELECT {complex_return_str} FROM combined;
            """
        else:
            return_select_str = "SELECT * FROM inserted"

        field_names = ", ".join(field_names_to_value_strs.keys())
        values = ", ".join(field_names_to_value_strs.values())

        q = f"""
WITH inserted AS (
    INSERT INTO {self._table_name} ({field_names})
    VALUES ({values})
    {conflict_str}
    RETURNING {self._returning_str}
)
{return_select_str}
            """

        return q, variables

    def build_insert_many_q_and_v(
        self, inserts: list[Insert], conflict: Conflict | None = None
    ) -> tuple[str, T.Any]:
        if self._qb.where or self._qb.from_:
            raise ResolverError("Resolver cannot have filters set for inserts.")

        prev_field_names_to_value_strs: dict[str, str] | None = None
        field_names_to_value_strs_list: list[dict[str, str]] = []
        variables_list: list[dict[str, T.Any]] = []
        for insert in inserts:
            # do not need to check that variables have the same keys since that is taken care of
            # with prev_field_names_to_value_strs comparisons
            field_names_to_value_strs, variables = self.parse_mutation_model(
                model=insert
            )
            if prev_field_names_to_value_strs is None:
                prev_field_names_to_value_strs = field_names_to_value_strs
            else:
                if field_names_to_value_strs != prev_field_names_to_value_strs:
                    raise ResolverError(
                        "All inserts must have the same fields to insert, including the same raw_sql."
                    )

            field_names_to_value_strs_list.append(field_names_to_value_strs)
            variables_list.append(variables)

        # first, build insert string
        fields_name_strs: list[str] = []
        select_val_strs: list[str] = []
        first_field_names_to_value_strs = field_names_to_value_strs_list[0]
        first_variables = variables_list[0]
        for col in self._node.__columns_in_order__:
            _values: list[T.Any] = []
            if col in first_field_names_to_value_strs:
                fields_name_strs.append(col)
                if col in first_variables:
                    select_val_strs.append(f"o.{col}")
                else:
                    # if it isn't a variable, add the value (from raw_sql) directly
                    select_val_strs.append(first_field_names_to_value_strs[col])

        patch_variables = {}
        conflict_str, patch_variables = self.build_conflict_str(
            conflict=conflict, existing_variables=patch_variables
        )

        return_select_str = "SELECT * FROM inserted"

        if (
            conflict_str
            and conflict.action == ConflictAction.DO_NOTHING
            and conflict.return_conflicting_rows
        ):
            # this means that you will have to return a UNION of the conflicts AND the returnings
            conflict_column_names = conflict.unique_column_names()
            conflict_col_names_str = ", ".join(
                [f"o.{n}" for n in conflict_column_names]
            )
            where_unique_index_str = conflict.unique_index_str
            if len(conflict_column_names) == 1:
                where_unique_index_str = conflict.unique_index_str.replace(
                    "(", ""
                ).replace(")", "")
            conflicting_from_str = f"{self._table_name} WHERE {where_unique_index_str} in (SELECT {conflict_col_names_str} FROM unnest($1::{self._table_name}[]) as o)) UNION ({return_select_str})"
            complex_return_str = self._returning_str_complex(use_table_name=False)
            return_select_str = f"""
, combined AS (
    SELECT {complex_return_str} FROM inserted
    UNION ALL
    SELECT {complex_return_str} FROM {conflicting_from_str}
    AND NOT EXISTS (SELECT 1 FROM inserted)
)
SELECT {complex_return_str} FROM combined;
                        """

        q = f"""
WITH inserted as (
    INSERT INTO {self._table_name} ({', '.join(fields_name_strs)})
    (SELECT {', '.join(select_val_strs)} FROM unnest((:_raw_models)::{self._table_name}[]) as o)
    {conflict_str}
    RETURNING {self._returning_str}
)
{return_select_str}
            """

        values: list[tuple[T.Any, ...]] = []
        for field_names_to_value_strs, variables in zip(
            field_names_to_value_strs_list, variables_list
        ):
            _values: list[T.Any] = []
            for col in self._node.__columns_in_order__:
                if col in field_names_to_value_strs and col in variables:
                    _v = variables[col]
                else:
                    _v = None
                _values.append(_v)

            values.append(tuple(_values))

        return q, {"_raw_models": values, **patch_variables}

    def build_patch_q_and_v(
        self, patch: Patch, patch_all: bool
    ) -> tuple[str, dict[str, T.Any]]:
        field_names_to_value_strs, variables = self.parse_mutation_model(model=patch)
        set_strs: list[str] = []

        for field_name, value in field_names_to_value_strs.items():
            set_strs.append(f"{field_name} = {value}")

        if not patch_all:
            if not self._qb.where:
                raise ResolverError(
                    "Unless you want to patch all rows (patch_all=True), you need to give a WHERE clause."
                )

        where_s = self._qb.replace_current_and_parent(
            s=f"WHERE {self._qb.where}",
            table_alias=self._table_name,
            parent_table_alias=None,
        )
        where_s, where_v = self._qb.prepare_query_sqlalchemy(
            sql=where_s, params=self._qb.variables
        )
        for k, v in where_v.items():
            if k in variables and v != variables[k]:
                raise ResolverError(f"Variables {k} is already being used.")
            variables[k] = v

        q = f"""
UPDATE {self._table_name} SET {', '.join(set_strs)}
{where_s.replace('$current.', f'{self._table_name}.')}
RETURNING {self._returning_str}
            """

        return q, variables

    def build_delete_q_and_v(self, delete_all: bool) -> tuple[str, dict[str, T.Any]]:
        if not delete_all:
            if not self._qb.where:
                raise ResolverError(
                    "Unless you want to delete all rows (delete_all=True), you need to give a WHERE clause."
                )

        where_s = self._qb.replace_current_and_parent(
            s=f"WHERE {self._qb.where}",
            table_alias=self._table_name,
            parent_table_alias=None,
        )
        where_s, where_v = self._qb.prepare_query_sqlalchemy(
            sql=where_s, params=self._qb.variables
        )

        q = f"""
DELETE FROM {self._table_name}
{where_s.replace('$current.', f'{self._table_name}.')}
RETURNING {self._returning_str}
                """

        return q, where_v

    @property
    def _table_name(self) -> str:
        return f'"{self._node.__table_name__}"'

    @property
    def _returning_str(self) -> str:
        """assume primary keys are not computed or complex paths"""
        returning_str = "*"
        returning_strs: set[str] = set()
        # include fields to include as long as the path == name or $current.name
        for primary_key in self._node.__primary_keys__:
            returning_strs.add(f"{self._table_name}.{primary_key} as {primary_key}")
        for sel in self._qb.selections:
            if sel.is_simple_column:
                returning_strs.add(f"{self._table_name}.{sel.name} as {sel.name}")
        if returning_strs:
            returning_str = ", ".join(sorted(returning_strs))
        return returning_str

    def _returning_str_complex(self, use_table_name: bool) -> str:
        returning_str = "*"
        returning_strs: set[str] = set()
        # include fields to include as long as the path == name or $current.name
        for primary_key in self._node.__primary_keys__:
            if use_table_name:
                returning_strs.add(f"{self._table_name}.{primary_key} as {primary_key}")
            else:
                returning_strs.add(primary_key)
        for sel in self._qb.selections:
            if sel.is_simple_column:
                if use_table_name:
                    returning_strs.add(f"{self._table_name}.{sel.name} as {sel.name}")
                else:
                    returning_strs.add(sel.name)
        if returning_strs:
            returning_str = ", ".join(sorted(returning_strs))
        return returning_str

    async def node_from_raw_val(
        self,
        raw_val: RowMapping,
        conn: AsyncConnection | None,
        format_sql: bool,
        commit_after: bool,
        force_refresh: bool,
        error_if_need_to_refresh: bool = False,
    ) -> NodeType:
        if conn and commit_after:
            logger.debug("[COMMIT AFTER]")
            await conn.commit()
        # for now, if there are selections other than id, refresh
        should_refresh = force_refresh
        if not should_refresh:
            for s in self._qb.selections:
                if s.name not in raw_val or not s.is_simple_column:
                    should_refresh = True
                    break
        if should_refresh:
            if error_if_need_to_refresh:
                raise ResolverError(
                    "This resolver requires a refresh but the node was deleted."
                )
            logger.debug("[REFRESH AFTER]")
            # what about composite primary keys? Or no primary keys?
            kwargs = {k: raw_val[k] for k in self._node.__primary_keys__}
            return await self._gerror(conn=conn, **kwargs)
        else:
            parsed_d: dict[str, T.Any] = {}
            for k, v in raw_val.items():
                if k not in self._node.__computed_columns__:
                    parsed_d[k] = v
            return self.parse_node(**parsed_d)

    async def nodes_from_raw_vals(
        self,
        raw_vals: T.Sequence[RowMapping],
        conn: AsyncConnection | None,
        format_sql: bool,
        commit_after: bool,
        force_refresh: bool,
        error_if_need_to_refresh: bool = False,
    ) -> list[NodeType]:
        if conn and commit_after:
            logger.debug("[COMMIT AFTER]")
            await conn.commit()
        # for now, if there are selections other than id, refresh
        should_refresh = force_refresh
        if not should_refresh:
            for raw_val in raw_vals:
                for s in self._qb.selections:
                    if s.name not in raw_val or not s.is_simple_column:
                        should_refresh = True
                        break
        if should_refresh:
            if error_if_need_to_refresh:
                raise ResolverError(
                    "This resolver requires a refresh but the node was deleted."
                )
            logger.debug("[REFRESH AFTER]")
            # what about composite primary keys? Or no primary keys?
            kwargs = {
                k: [raw_val[k] for raw_val in raw_vals]
                for k in self._node.__primary_keys__
            }
            return await self._filter_in(**kwargs)._query(
                format_sql=format_sql, conn=conn, log_query=True
            )
        else:
            nodes: list[NodeType] = []
            for raw_val in raw_vals:
                parsed_d: dict[str, T.Any] = {}
                for k, v in raw_val.items():
                    if k not in self._node.__computed_columns__:
                        parsed_d[k] = v
                nodes.append(self.parse_node(**parsed_d))
            return nodes

    async def insert_one_or_none(
        self,
        insert: Insert,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_insert: bool = False,
        force_refresh: bool = False,
        conflict: Conflict | None = None,
    ) -> NodeType | None:
        q, v = self.build_insert_q_and_v(insert=insert, conflict=conflict)
        raw_val = await sql_pool.query_record(q, v, log_query=log_query, conn=conn)
        if conn and commit_after_insert:
            logger.debug("insert committing")
            await conn.commit()
        if not raw_val:
            return None
        return await self.node_from_raw_val(
            raw_val=raw_val,
            conn=conn,
            format_sql=format_sql,
            commit_after=commit_after_insert,
            force_refresh=force_refresh,
        )

    async def insert_one(
        self,
        insert: Insert,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_insert: bool = False,
        force_refresh: bool = False,
        conflict: Conflict | None = None,
    ) -> NodeType:
        if conflict and conflict.return_conflicting_rows is not True:
            raise ResolverError(
                "If you want to insert_one with a conflict, conflict.return_conflicting_rows must be True. "
                "Otherwise, choose insert_one_or_none."
            )
        node = await self.insert_one_or_none(
            insert=insert,
            format_sql=format_sql,
            log_query=log_query,
            conn=conn,
            commit_after_insert=commit_after_insert,
            force_refresh=force_refresh,
            conflict=conflict,
        )
        if not node:
            raise ResolverError("Nothing was inserted.")
        return node

    async def insert_many(
        self,
        inserts: list[Insert],
        conflict: Conflict | None = None,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_insert: bool = False,
        force_refresh: bool = False,
    ) -> list[NodeType]:
        """If you want to try returning in the same query, see the deleted code that tried to do it:
        ff4491b..ad721c4  main -> main"""
        if not inserts:
            return []
        q, v = self.build_insert_many_q_and_v(inserts=inserts, conflict=conflict)
        raw_vals = await sql_pool.query_records(q, v, log_query=log_query, conn=conn)
        return await self.nodes_from_raw_vals(
            raw_vals=raw_vals,
            conn=conn,
            format_sql=format_sql,
            commit_after=commit_after_insert,
            force_refresh=force_refresh,
        )

    async def patch_many(
        self,
        patch: Patch,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_patch: bool = False,
        force_refresh: bool = False,
        patch_all: bool = False,
    ) -> list[NodeType]:
        q, v = self.build_patch_q_and_v(patch=patch, patch_all=patch_all)
        raw_vals = await sql_pool.query_records(q, v, log_query=log_query, conn=conn)
        return await self.nodes_from_raw_vals(
            raw_vals=raw_vals,
            conn=conn,
            format_sql=format_sql,
            commit_after=commit_after_patch,
            force_refresh=force_refresh,
        )

    async def patch_one(
        self,
        patch: Patch,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_patch: bool = False,
        force_refresh: bool = False,
    ) -> NodeType:
        q, v = self.build_patch_q_and_v(patch=patch, patch_all=False)
        if conn:
            raw_val = await sql_pool.query_records(
                q, v, log_query=log_query, conn=conn, confirm_only_one=True
            )
        else:
            raw_val = await sql_pool.query_records(
                q, v, log_query=log_query, confirm_only_one=True
            )
        return await self.node_from_raw_val(
            raw_val=raw_val,
            conn=conn,
            format_sql=format_sql,
            commit_after=commit_after_patch,
            force_refresh=force_refresh,
        )

    async def delete_one_or_none(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_delete: bool = False,
    ) -> NodeType | None:
        q, v = self.build_delete_q_and_v(delete_all=False)
        try:
            if conn:
                raw_val = await sql_pool.query_records(
                    q, v, log_query=log_query, conn=conn, confirm_only_one=True
                )
            else:
                raw_val = await sql_pool.query_records(
                    q, v, log_query=log_query, confirm_only_one=True
                )
        except NoRowsReturnedError:
            return None
        return await self.node_from_raw_val(
            raw_val=raw_val,
            conn=conn,
            format_sql=format_sql,
            commit_after=commit_after_delete,
            force_refresh=False,
            error_if_need_to_refresh=True,
        )

    async def delete_one(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_delete: bool = False,
    ) -> NodeType:
        row = await self.delete_one_or_none(
            format_sql=format_sql,
            log_query=log_query,
            conn=conn,
            commit_after_delete=commit_after_delete,
        )
        if not row:
            raise ResolverError("No rows were deleted.")
        return row

    async def delete_many(
        self,
        *,
        format_sql: bool = False,
        log_query: bool = False,
        conn: AsyncConnection | None = None,
        commit_after_delete: bool = False,
        delete_all: bool = False,
    ) -> list[NodeType]:
        q, v = self.build_delete_q_and_v(delete_all=delete_all)
        raw_vals = await sql_pool.query_records(q, v, log_query=log_query, conn=conn)
        return await self.nodes_from_raw_vals(
            raw_vals=raw_vals,
            conn=conn,
            format_sql=format_sql,
            commit_after=commit_after_delete,
            force_refresh=False,
            error_if_need_to_refresh=True,
        )

    def parse_node(self, **kwargs) -> NodeType:
        node = self._node(**kwargs)
        # do computeds here
        if self._runtime__computed_columns__:
            for name, col in self._runtime__computed_columns__.items():
                if name not in kwargs:
                    raise ResolverError(f"Computed column {name} not found in results.")
                computed_val = kwargs[name]
                if computed_val is None:
                    if not col.is_nullable:
                        raise ResolverError(
                            f"Computed column {name} is not nullable but was null."
                        )
                else:
                    if col.custom_converter:
                        computed_val = col.custom_converter(computed_val)
                    else:
                        if col.data_type not in TYPES_MAP:
                            raise ResolverError(
                                f"You must either give a custom converter or a valid data_type for computed column {name}."
                            )
                        type_map_val = TYPES_MAP[col.data_type]
                        if col.cardinality == Cardinality.ONE:
                            if not isinstance(computed_val, type_map_val.val):
                                computed_val = type_map_val.serializer(computed_val)
                        else:
                            computed_val_list = []
                            for v in computed_val:
                                if not isinstance(v, type_map_val.val):
                                    v = type_map_val.serializer(v)
                                computed_val_list.append(v)
                            computed_val = computed_val_list
                node.computed[name] = computed_val

        # now do nested
        for key, edge in self._children.items():
            raw_child = kwargs[key]
            if edge.cardinality == Cardinality.ONE:
                if raw_child is None:
                    if edge.is_required:
                        raise ResolverError(f"{key} is required but is null.")
                    node._children_cache[key] = None
                else:
                    node._children_cache[key] = edge.resolver.parse_node(**raw_child)
            else:
                node._children_cache[key] = [
                    edge.resolver.parse_node(**d) for d in raw_child
                ]

        # TODO extras later

        return node


def validate_get_kwargs(**kwargs) -> tuple[str, T.Any]:
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    kwargs_len = len(kwargs)
    if kwargs_len != 1:
        raise ResolverError(
            f"Must only give one argument, received {kwargs_len} arguments: {kwargs}."
        )
    field_name, value = list(kwargs.items())[0]
    return field_name, value


ResolverType = T.TypeVar("ResolverType", bound=Resolver)
ThisResolverType = ResolverType
