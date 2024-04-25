import typing as T
from uuid import UUID
from datetime import date, datetime, time
from pydantic import BaseModel


class TypeData(BaseModel):
    name: str
    val: T.Type
    serializer: T.Callable


TYPES_MAP: dict[str, TypeData] = {
    "uuid": TypeData(name="UUID", val=UUID, serializer=UUID),
    "double precision": TypeData(name="float", val=float, serializer=float),
    "float": TypeData(name="float", val=float, serializer=float),
    "date": TypeData(name="datetime.date", val=date, serializer=date.fromisoformat),
    "timestamp with time zone": TypeData(
        name="datetime.datetime", val=datetime, serializer=datetime.fromisoformat
    ),
    "timestamp": TypeData(
        name="datetime.datetime", val=datetime, serializer=datetime.fromisoformat
    ),
    "datetime": TypeData(
        name="datetime.datetime", val=datetime, serializer=datetime.fromisoformat
    ),
    "time": TypeData(name="datetime.time", val=time, serializer=time.fromisoformat),
    "time without time zone": TypeData(
        name="datetime.time", val=time, serializer=time.fromisoformat
    ),
    "character varying": TypeData(name="str", val=str, serializer=str),
    "boolean": TypeData(name="bool", val=bool, serializer=bool),
    "bool": TypeData(name="bool", val=bool, serializer=bool),
    "integer": TypeData(name="int", val=int, serializer=int),
    "int": TypeData(name="int", val=int, serializer=int),
    "text": TypeData(name="str", val=str, serializer=str),
    "varchar": TypeData(name="str", val=str, serializer=str),
    "str": TypeData(name="str", val=str, serializer=str),
    "jsonb": TypeData(name="dict", val=dict, serializer=dict),
    "json": TypeData(name="dict", val=dict, serializer=dict),
}

__all__ = ["TypeData", "TYPES_MAP"]
