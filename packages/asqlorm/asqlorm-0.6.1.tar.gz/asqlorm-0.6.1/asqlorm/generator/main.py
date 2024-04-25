import typing as T
import re
from black import format_str, FileMode
from pydantic import BaseModel, Field
import psycopg

from asqlorm.utils import TYPES_MAP
from asqlorm.models import (
    Node,
    Resolver,
    ComputedColumn,
    Cardinality,
    ComputedLink,
)


class GeneratorError(Exception):
    pass


class TableConfig(BaseModel):
    base_node: T.Type[Node] | None = None
    base_resolver: T.Type[Resolver] | None = None
    # columns_to_default_include: set[str] = Field(default_factory=set)


class Ref(BaseModel):
    table_name: str
    column_name: str
    is_nullable: bool

    @classmethod
    def from_str(cls, s: str, is_nullable: bool):
        ref_table_name = s[: s.index("(")]
        ref_col_name = s[s.index("(") + 1 : s.index(")")]
        return cls(
            table_name=ref_table_name, column_name=ref_col_name, is_nullable=is_nullable
        )


DEFAULT_ENUMS_QUERY: str = """
SELECT n.nspname   AS schema_name,
       t.typname   AS enum_type,
       e.enumlabel AS enum_value
FROM pg_type t
         JOIN
     pg_enum e ON t.oid = e.enumtypid
         JOIN
     pg_catalog.pg_namespace n ON n.oid = t.typnamespace
WHERE n.nspname = 'public'
ORDER BY t.typname,
         e.enumsortorder;
"""

DEFAULT_COLUMNS_QUERY: str = """
SELECT col.table_schema,
       col.table_name,
       col.column_name,
       CASE
           WHEN col.data_type = 'ARRAY' THEN array_type.typname || '[]'
           WHEN col.data_type = 'USER-DEFINED' THEN pg_type.typname
           ELSE col.data_type
       END as data_type,
       CASE
           WHEN col.is_nullable = 'YES' THEN true
           ELSE false
       END as is_nullable,
       col.column_default as default_value, -- Added default value column
       (SELECT string_agg(DISTINCT cons_info, '; ')
        FROM (
              SELECT tc.constraint_type || ': ' || tc.constraint_name ||
                     CASE
                         WHEN tc.constraint_type = 'FOREIGN KEY'
                             THEN ' references ' || ccu.table_name || '(' || ccu.column_name || ')'
                         ELSE ''
                         END AS cons_info
              FROM information_schema.table_constraints tc
                       JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                       AND tc.table_schema = kcu.table_schema
                       AND tc.table_name = kcu.table_name
                       LEFT JOIN information_schema.constraint_column_usage ccu
                             ON ccu.constraint_name = tc.constraint_name
                             AND ccu.table_schema = tc.table_schema
              WHERE kcu.column_name = col.column_name
                AND kcu.table_name = col.table_name
                AND kcu.table_schema = col.table_schema

              UNION ALL

              SELECT 'UNIQUE INDEX: ' || idx.relname AS cons_info
              FROM pg_index
                       JOIN pg_class idx ON pg_index.indexrelid = idx.oid
                       JOIN pg_class tbl ON pg_index.indrelid = tbl.oid
                       JOIN pg_namespace ns ON tbl.relnamespace = ns.oid
                       JOIN pg_attribute attr ON attr.attrelid = tbl.oid AND attr.attnum = ANY(pg_index.indkey)
              WHERE pg_index.indisunique = true
                AND ns.nspname = col.table_schema
                AND tbl.relname = col.table_name
                AND attr.attname = col.column_name
                AND (SELECT COUNT(*) FROM pg_attribute WHERE attrelid = tbl.oid AND attnum = ANY(pg_index.indkey)) = 1
        ) AS detailed_constraints) AS constraints_info
FROM information_schema.columns col
         LEFT JOIN pg_type ON col.udt_name = pg_type.typname
         LEFT JOIN pg_type array_type ON pg_type.typelem = array_type.oid
WHERE col.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY col.table_schema, col.table_name, col.ordinal_position;
"""

DEFAULT_TABLES_QUERY = """
SELECT
    n.nspname AS schema_name,
    c.relname AS table_name,
    d.description AS comment,
    (
        SELECT string_agg(cons.constr_details, '; ')
        FROM (
            SELECT
                CASE pc.contype
                    WHEN 'p' THEN 'PRIMARY KEY (' || pg_get_constraintdef(pc.oid) || ')'
                    WHEN 'f' THEN 'FOREIGN KEY (' || pg_get_constraintdef(pc.oid) || ')'
                    WHEN 'u' THEN 'UNIQUE (' || pg_get_constraintdef(pc.oid) || ')'
                    WHEN 'c' THEN 'CHECK (' || pg_get_constraintdef(pc.oid) || ')'
                    WHEN 'x' THEN 'EXCLUDE (' || pg_get_constraintdef(pc.oid) || ')'
                    ELSE 'OTHER'
                END AS constr_details
            FROM pg_constraint pc
            WHERE pc.conrelid = c.oid
        ) cons
    ) AS constraints
FROM
    pg_class c
JOIN
    pg_namespace n ON c.relnamespace = n.oid
LEFT JOIN
    pg_description d ON c.oid = d.objoid
WHERE
    c.relkind = 'r' -- 'r' indicates a regular table
    AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY
    n.nspname,
    c.relname;
"""


def convert_to_variable_name(enum_name: str) -> str:
    return re.sub(r"\W|^(?=\d)", "_", enum_name)


def build_enums_str(
    *,
    db_dsn: str,
    custom_query: str = DEFAULT_ENUMS_QUERY,
    custom_enum_converter: T.Callable[[str], str] = None,
) -> str:
    enum_converter = custom_enum_converter or convert_to_variable_name
    enums_d: dict[str, list[str]] = {}
    with psycopg.connect(db_dsn) as conn:
        conn.row_factory = psycopg.rows.dict_row
        with conn.cursor() as cur:
            cur.execute(custom_query)
            for record in cur.fetchall():
                enum_type = record["enum_type"]
                if enum_type not in enums_d:
                    enums_d[enum_type] = []
                enums_d[enum_type].append(record["enum_value"])
    # now build the python string from this
    enum_strs: list[str] = []
    for enum_name, enum_values in enums_d.items():
        enum_values_str = "\n".join(
            [f'\t{enum_converter(v)} = "{v}"' for v in enum_values]
        )
        enum_strs.append(
            f"""
class {enum_name}(str, Enum):
{enum_values_str}
        """.strip()
        )
    all_strs = ["from enum import Enum", *enum_strs]
    enum_str = "\n".join(all_strs)
    return format_str(enum_str, mode=FileMode())


class Column(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    constraints_info: str | None

    basemodel_type: T.Type[BaseModel] | None = None
    cardinality: Cardinality = Cardinality.ONE

    default_value: str | None = None

    original_column: T.Optional["Column"] = None
    computed_column: T.Optional["ComputedColumn"] = None


class Table(BaseModel):
    name: str
    comment: str | None
    columns: list[Column] = Field(default_factory=list)
    constraints: str | None = None

    def __hash__(self):
        return hash(self.name)


def build_nodes_and_resolvers_str(
    *,
    db_dsn: str,
    base_node: T.Type[Node] | None = None,
    base_resolver: T.Type[Resolver] | None = None,
    configs_by_table_name: dict[str, TableConfig],
    custom_columns_query: str = DEFAULT_COLUMNS_QUERY,
    custom_tables_query: str = DEFAULT_TABLES_QUERY,
) -> str:
    # first get columns
    ordered_columns_by_table_name: dict[str, list[str]] = {}
    tables_by_name: dict[str, Table] = {}
    with psycopg.connect(db_dsn) as conn:
        conn.row_factory = psycopg.rows.dict_row
        with conn.cursor() as cur:
            cur.execute(custom_tables_query)
            for record in cur.fetchall():
                table_name = record["table_name"]
                table = Table(
                    name=table_name,
                    comment=record["comment"],
                    constraints=record["constraints"],
                )
                tables_by_name[table_name] = table
            cur.execute(custom_columns_query)
            for record in cur.fetchall():
                table_name = record["table_name"]
                tables_by_name[table_name].columns.append(
                    Column(
                        name=record["column_name"],
                        data_type=record["data_type"],
                        is_nullable=record["is_nullable"],
                        constraints_info=record["constraints_info"],
                        default_value=record["default_value"],
                    )
                )
                if table_name not in ordered_columns_by_table_name:
                    ordered_columns_by_table_name[table_name] = []
                ordered_columns_by_table_name[table_name].append(record["column_name"])

    mixin_strs: list[str] = []
    node_strs: list[str] = []
    insert_strs: list[str] = []
    patch_strs: list[str] = []
    resolver_strs: list[str] = []

    if base_node:
        base_node_name = f"{base_node.__name__}__"
        mixin_strs.append(
            f"from {base_node.__module__} import {base_node.__name__} as {base_node_name}"
        )
    else:
        base_node_name = "Node"

    if base_resolver:
        base_resolver_name = f"{base_resolver.__name__}__"
        mixin_strs.append(
            f"from {base_resolver.__module__} import {base_resolver.__name__} as {base_resolver_name}"
        )
    else:
        base_resolver_name = "Resolver"

    for table in tables_by_name.values():
        # table config first
        table_config = configs_by_table_name.get(table.name)
        base_node_import_name: str | None = None
        base_resolver_import_name: str | None = None
        computed_columns_str = (
            "\t__computed_columns__: T.ClassVar[dict[str, ComputedColumn]] = {}"
        )
        table_name_str = f'\t__table_name__: T.ClassVar[str] = "{table.name}"'
        ordered_cols_str = ", ".join(
            [f'"{f}"' for f in ordered_columns_by_table_name[table.name]]
        )
        columns_in_order_str = (
            f"\t__columns_in_order__: T.ClassVar[list[str]] = [{ordered_cols_str}]"
        )
        computed_links: dict[str, ComputedLink] = {}
        if table_config:
            if table_config.base_node:
                if not hasattr(table_config.base_node, "__computed_columns__"):
                    table_config.base_node.__computed_columns__ = {}
                if not hasattr(table_config.base_node, "__computed_links__"):
                    table_config.base_node.__computed_links__ = {}
                computed_links = table_config.base_node.__computed_links__
                computed_columns_str = ""
                base_node_import_name = f"{table_config.base_node.__name__}__"
                mixin_strs.append(
                    f"from {table_config.base_node.__module__} import {table_config.base_node.__name__} as {base_node_import_name}"
                )
                # get the computed and default columns
                columns_by_name: dict[str, Column] = {c.name: c for c in table.columns}
                for (
                    computed_name,
                    computed_c,
                ) in table_config.base_node.__computed_columns__.items():
                    original_column: Column | None = None
                    computed_c: ComputedColumn
                    # computed names will overwrite given ones
                    if computed_name in columns_by_name:
                        if not computed_c.override:
                            raise GeneratorError(
                                f"Computed colum {computed_name} is already a column. "
                                f"If you want to override it, set override=True on the ComputedColumn."
                            )
                        col_to_remove = columns_by_name[computed_name]
                        original_column = col_to_remove
                        table.columns.remove(col_to_remove)

                    if computed_c.basemodel_type:
                        import_s = f"from {computed_c.basemodel_type.__module__} import {computed_c.basemodel_type.__name__} as {computed_c.basemodel_type.__name__}__"
                        if import_s not in mixin_strs:
                            mixin_strs.append(import_s)

                    table.columns.append(
                        Column(
                            name=computed_name,
                            data_type=computed_c.data_type,
                            is_nullable=computed_c.is_nullable,
                            constraints_info=None,
                            basemodel_type=computed_c.basemodel_type,
                            cardinality=computed_c.cardinality,
                            original_column=original_column,
                            computed_column=computed_c,
                        )
                    )
            if table_config.base_resolver:
                base_resolver_import_name = f"{table_config.base_resolver.__name__}__"
                mixin_strs.append(
                    f"from {table_config.base_resolver.__module__} import {table_config.base_resolver.__name__} as {base_resolver_import_name}"
                )

        safe_table_name = convert_to_variable_name(table.name)
        get_params: set[str] = set()
        primary_keys: list[str] = []

        # first, add composite keys to get params
        if table.constraints:
            matches = re.findall(
                r"PRIMARY KEY \(PRIMARY KEY \((.*?)\)", table.constraints
            )
            if matches:
                if len(matches) > 1:
                    raise GeneratorError(
                        f"Found more than one primary key for table {table.name}."
                    )
                primary_keys = matches[0].split(", ")

        inner_primary_keys = [f'"{p}"' for p in primary_keys]
        primary_keys_str = f"\t__primary_keys__: T.ClassVar[list[str]] = [{', '.join(inner_primary_keys)}]"

        col_names_to_refs: dict[str, Ref] = {}
        col_strs: list[str] = []
        insert_fields_strs: list[str] = []
        patch_fields_strs: list[str] = []
        filter_by_strs: list[str] = []
        filter_in_strs: list[str] = []
        col_name_to_anno: dict[str, str] = {}
        for col in table.columns:
            if col.data_type.endswith("[]"):
                is_list = True
                data_type = col.data_type.replace("[]", "")
            else:
                is_list = False
                data_type = col.data_type
            if col.basemodel_type:
                python_anno = f"{col.basemodel_type.__name__}__"
            else:
                if data_type in TYPES_MAP:
                    python_anno = TYPES_MAP[data_type].name
                else:
                    # this is an enum
                    python_anno = f"enums.{data_type}"
            if is_list:
                python_anno = f"list[{python_anno}]"
            if col.cardinality == Cardinality.MANY:
                python_anno = f"list[{python_anno}]"
            if col.is_nullable:
                python_anno = f"{python_anno} | None"
            col_strs.append(f"{col.name}: {python_anno} = None")
            if not col.basemodel_type:
                filter_by_strs.append(
                    f"{col.name}: T.Union[{python_anno}, UNSET] = UNSET"
                )
                filter_in_strs.append(
                    f"{col.name}: T.Union[list[{python_anno}], UNSET] = UNSET"
                )
            col_name_to_anno[col.name] = python_anno
            # handle constraints now
            if col.constraints_info:
                constraints = [c.strip() for c in col.constraints_info.split(";")]
                for constraint in constraints:
                    if constraint.startswith("UNIQUE:") or constraint.startswith(
                        "UNIQUE INDEX:"
                    ):
                        if not col.is_nullable:
                            get_params.add(f"{col.name}: {python_anno} = None")
                    elif constraint.startswith("FOREIGN KEY:"):
                        col_names_to_refs[col.name] = Ref.from_str(
                            s=constraint[constraint.index("references ") + 11 :],
                            is_nullable=col.is_nullable,
                        )
                    elif constraint.startswith("PRIMARY KEY:"):
                        # handling this later
                        continue
                    else:
                        raise GeneratorError(f"Invalid constraint: {constraint=}")

            python_anno_insert = f"T.Union[{python_anno}, raw_sql]"
            python_anno_patch = f"T.Optional[T.Union[{python_anno}, raw_sql]]"

            # if computed, ignore
            # if computed and has original col, keep
            if (
                table_config
                and table_config.base_node
                and col.name in table_config.base_node.__computed_columns__
            ):
                if col.original_column:
                    insert_fields_strs.append(
                        f'{col.name}: {python_anno_insert}{" = None" if col.original_column.is_nullable or col.original_column.default_value else ""}'
                    )
            else:
                insert_fields_strs.append(
                    f'{col.name}: {python_anno_insert}{" = None" if col.is_nullable or col.default_value else ""}'
                )
            if col.name not in primary_keys:
                patch_fields_strs.append(f"{col.name}: {python_anno_patch} = None")

        # now add get params for primary keys
        if primary_keys:
            if len(primary_keys) == 1:
                primary_key = primary_keys[0]
                get_params.add(f"{primary_key}: {col_name_to_anno[primary_key]} = None")
            else:
                combined_anno_strs: list[str] = []
                for primary_key in primary_keys:
                    combined_anno_strs.append(col_name_to_anno[primary_key])
                get_params.add(
                    f'{"__".join(primary_keys)}: tuple[{", ".join(combined_anno_strs)}] = None'
                )

        # build filter params
        filter_by_strs.sort()
        filter_in_strs.sort()

        filter_by_params_str = ", ".join(filter_by_strs)
        filter_by_inner_params = ", ".join(
            [f"{n.split(':')[0]}={n.split(':')[0]}" for n in filter_by_strs]
        )

        filter_in_params_str = ", ".join(filter_in_strs)
        filter_in_inner_params = ", ".join(
            [f"{n.split(':')[0]}={n.split(':')[0]}" for n in filter_by_strs]
        )

        # build resolver functions like artist()
        # AND build node functions like artist() -> Artist
        resolver_func_strs: list[str] = []
        node_func_strs: list[str] = []
        for c_name, ref in col_names_to_refs.items():
            safe_c_name = convert_to_variable_name(c_name)
            c_name_key = f"_{ref.column_name}"
            if c_name_key in safe_c_name:
                safe_c_name = safe_c_name[: safe_c_name.rindex(f"_{ref.column_name}")]
            else:
                safe_c_name = f"{safe_c_name}_"
            safe_target_table_name = convert_to_variable_name(ref.table_name)
            safe_rez_name = f"{safe_target_table_name}Resolver"
            resolver_func_strs.append(
                f"""
    def {safe_c_name}(self, resolver: T.Optional["{safe_rez_name}"] = None, key: str = "{safe_c_name}") -> "{safe_table_name}Resolver":
        self.add_child(
            key=key,
            resolver = resolver or {safe_rez_name}(),
            cardinality=Cardinality.ONE,
            from_='FROM "{ref.table_name}" $current WHERE $current.{ref.column_name} = $parent.{c_name}',
            is_required={'True' if not ref.is_nullable else 'False'}
        )
        return self
            """
            )
            node_func_strs.append(
                f'def {safe_c_name}(self, key: str = "{safe_c_name}") -> "{safe_target_table_name}": return self._resolve_node(key=key)'
            )
        for link_name, link in computed_links.items():
            target_rez_name = f"{link.node_name}Resolver"
            kwargs_strs: list[str] = []
            if link.annotations_by_kwarg:
                for var_name, var_anno in link.annotations_by_kwarg.items():
                    kwargs_strs.append(f"{var_name}: {var_anno}")

            kwargs_str = ""
            update_qb_str = ""
            if kwargs_strs:
                kwargs_str = ", *, " + ", ".join(kwargs_strs)
            if link.update_qb:
                if link.annotations_by_kwarg:
                    names_str = ", " + ", ".join(
                        [f"{n}={n}" for n in link.annotations_by_kwarg.keys()]
                    )
                else:
                    names_str = ""
                update_qb_str = f"self._node.__computed_links__['{link_name}'].update_qb(self._qb{names_str})"
            resolver_func_strs.append(
                f"""
    def {link_name}(self, resolver: T.Optional["{target_rez_name}"] = None, key: str = "{link_name}"{kwargs_str}) -> "{safe_table_name}Resolver":
        self.add_child(
            key=key,
            resolver = resolver or {target_rez_name}(),
            cardinality={'Cardinality.ONE' if link.cardinality == Cardinality.ONE else 'Cardinality.MANY'},
            from_='{link.from_}',
            is_required={'False' if link.is_nullable else 'True'}
        )
        {update_qb_str}
        return self
            """
            )
            target_node_name = (
                f'"{link.node_name}"'
                if link.cardinality == Cardinality.ONE
                else f'list["{link.node_name}"]'
            )
            if link.is_nullable:
                target_node_name = f"T.Optional[{target_node_name}]"
            node_func_strs.append(
                f'def {link_name}(self, key: str = "{link_name}") -> {target_node_name}: return self._resolve_node(key=key)'
            )

        resolver_func_str = "\n".join(sorted(resolver_func_strs))
        node_func_str = "\n".join(sorted([f"\t{n}" for n in node_func_strs]))

        get_col_names = [p.split(":")[0] for p in get_params]
        get_inner_params = ", ".join(sorted([f"{n}={n}" for n in get_col_names]))
        col_str = "\n".join(sorted([f"\t{c}" for c in col_strs]))

        node_strs.append(
            f"""
class {safe_table_name}({base_node_import_name or base_node_name}):
{col_str}
{node_func_str}
{computed_columns_str}
{columns_in_order_str}
{table_name_str}
{primary_keys_str}
        """
        )
        insert_str = "\n".join(sorted([f"\t{c}" for c in insert_fields_strs]))
        insert_strs.append(
            f"""
class {safe_table_name}Insert(Insert):
{insert_str}
            """
        )
        if patch_fields_strs:
            patch_str = "\n".join(sorted([f"\t{c}" for c in patch_fields_strs]))
            patch_strs.append(
                f"""
class {safe_table_name}Patch(Patch):
{patch_str}
                """
            )

        if get_params:
            joined_get_params = ", ".join(sorted(get_params))
            get_strs = f"""
    async def get(self, conn: AsyncConnection | None = None, *, {joined_get_params}) -> {safe_table_name} | None:
        return await self._get(conn=conn, {get_inner_params})
    
    async def gerror(self, conn: AsyncConnection | None = None, *, {joined_get_params}) -> {safe_table_name}:
        return await self._gerror(conn=conn, {get_inner_params})
    
    async def query(self, conn: AsyncConnection | None = None, *, format_sql: bool = False, log_query: bool = False) -> list[{safe_table_name}]:
        return await self._query(conn=conn, format_sql=format_sql, log_query=log_query)
    
    async def first_or_none(self, conn: AsyncConnection | None = None, *, format_sql: bool = False, log_query: bool = False) -> {safe_table_name} | None:
        return await super().first_or_none(conn=conn, format_sql=format_sql, log_query=log_query)
    
    async def first(self, conn: AsyncConnection | None = None, *, format_sql: bool = False, log_query: bool = False) -> {safe_table_name}:
        return await super().first(conn=conn, format_sql=format_sql, log_query=log_query)
    
    async def one_or_none(self, conn: AsyncConnection | None = None, *, format_sql: bool = False, log_query: bool = False) -> {safe_table_name} | None:
        return await super().one_or_none(conn=conn, format_sql=format_sql, log_query=log_query)

    async def one(self, conn: AsyncConnection | None = None, *, format_sql: bool = False, log_query: bool = False) -> {safe_table_name}:
        return await super().one(conn=conn, format_sql=format_sql, log_query=log_query)
    
    def filter_by(self, *, {filter_by_params_str}) -> "{safe_table_name}Resolver":
        return self._filter_by({filter_by_inner_params})
    
    def filter_in(self, *, {filter_in_params_str}) -> "{safe_table_name}Resolver":
        return self._filter_in({filter_in_inner_params})
    
    async def insert_one(self, insert: {safe_table_name}Insert, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_insert: bool = False, force_refresh: bool = False, conflict: Conflict | None = None) -> {safe_table_name}:
        return await super().insert_one(insert=insert, format_sql=format_sql, log_query=log_query, conn=conn, commit_after_insert=commit_after_insert, force_refresh=force_refresh, conflict=conflict)
    
    async def insert_one_or_none(self, insert: {safe_table_name}Insert, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_insert: bool = False, force_refresh: bool = False, conflict: Conflict | None = None) -> T.Optional[{safe_table_name}]:
        return await super().insert_one_or_none(insert=insert, format_sql=format_sql, log_query=log_query, conn=conn, commit_after_insert=commit_after_insert, force_refresh=force_refresh, conflict=conflict)

    async def insert_many(self, inserts: list[{safe_table_name}Insert], conflict: Conflict | None = None, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_insert: bool = False, force_refresh: bool = False) -> list[{safe_table_name}]:
        return await super().insert_many(inserts=inserts, conflict=conflict, format_sql=format_sql, log_query=log_query, conn=conn, commit_after_insert=commit_after_insert, force_refresh=force_refresh)
    
    async def delete_one_or_none(self, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_delete: bool = False) -> T.Optional[{safe_table_name}]:
        return await super().delete_one_or_none(format_sql=format_sql, log_query=log_query, conn=conn, commit_after_delete=commit_after_delete)
    
    async def delete_one(self, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_delete: bool = False) -> {safe_table_name}:
        return await super().delete_one(format_sql=format_sql, log_query=log_query, conn=conn, commit_after_delete=commit_after_delete)
    
    async def delete_many(self, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_delete: bool = False, delete_all: bool = False) -> list[{safe_table_name}]:
        return await super().delete_many(format_sql=format_sql, log_query=log_query, conn=conn, commit_after_delete=commit_after_delete, delete_all=delete_all)
            """
            if patch_fields_strs:
                patch_one_str = f"""
    async def patch_one(self, patch: {safe_table_name}Patch, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_patch: bool = False, force_refresh: bool = False) -> {safe_table_name}:
        return await super().patch_one(patch=patch, format_sql=format_sql, log_query=log_query, conn=conn, commit_after_patch=commit_after_patch, force_refresh=force_refresh)
    
    async def patch_many(self, patch: {safe_table_name}Patch, *, format_sql: bool = False, log_query: bool = False, conn: AsyncConnection | None = None, commit_after_patch: bool = False, force_refresh: bool = False, patch_all: bool = False) -> list[{safe_table_name}]:
        return await super().patch_many(patch=patch, format_sql=format_sql, log_query=log_query, conn=conn, commit_after_patch=commit_after_patch, force_refresh=force_refresh, patch_all=patch_all)
                """
                get_strs = f"{get_strs}\n{patch_one_str}"
        else:
            get_strs = ""

        include_col_anno_strs: list[str] = []
        include_col_inner_strs: list[str] = []
        if table.columns:
            for col in table.columns:
                computed_c = col.computed_column
                if computed_c and computed_c.include_args_annotation:
                    anno = computed_c.include_args_annotation
                    if computed_c.is_nullable:
                        anno = f"T.Optional[{anno}]"
                    include_col_anno_strs.append(f"{col.name}: {anno} = UNSET")
                else:
                    include_col_anno_strs.append(f"{col.name}: bool = False")
                include_col_inner_strs.append(f"{col.name}={col.name}")

        if include_col_anno_strs:
            include_col_str: str = ", ".join(sorted(include_col_anno_strs))
            include_col_inner_strs: str = ", ".join(sorted(include_col_inner_strs))
            include_func_str = f'def include(self, *, {include_col_str}) -> "{safe_table_name}Resolver": return self._include({include_col_inner_strs})'
        else:
            include_func_str = ""

        resolver_strs.append(
            f"""
class {safe_table_name}Resolver({base_resolver_import_name or base_resolver_name}):
    _node = {safe_table_name}
    
{get_strs}
{resolver_func_str}
    {include_func_str}
        """
        )
    all_strs = [
        "import typing as T",
        "import datetime",
        "from uuid import UUID",
        "from pydantic_core import PydanticUndefined as UNSET",
        "from sqlalchemy.ext.asyncio import AsyncConnection",
        "from asqlorm.models import Node, Insert, Patch, Resolver, Conflict, ComputedColumn, raw_sql",
        "from fastgql.query_builders.sql.query_builder import Cardinality",
        "from . import enums",
        *mixin_strs,
        *sorted(node_strs),
        *sorted(insert_strs),
        *sorted(patch_strs),
        *sorted(resolver_strs),
    ]
    all_str = "\n".join(all_strs)
    return format_str(all_str, mode=FileMode())
