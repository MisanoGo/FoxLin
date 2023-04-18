from typing import List, Dict, Union, Callable

from pydantic import BaseModel as BsMdl

from .tog import TupleGraph
#from .den import Den

ID = str
COLUMN = str
LEVEL = str
DB_TYPE = Dict[COLUMN, TupleGraph]


class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True


class Schema(BaseModel):
    """
    databaser schema aliaser & also record carrier
    """
    ID: str | None = None


class DBCarrier(BaseModel):
    db: DB_TYPE | None = None


class Log(BaseModel):
    box_level: str
    log_level: str
    message: object = None


class DBOperation(BaseModel):
    """
    for manage operation in the different data management level of program,
    we use DBOperation to transfer operation between levels
    """
    op_name: str
    callback: Callable | None = None
    callback_level: LEVEL | None= None  # that level callback can call

    levels: List[LEVEL] = ['log']
    logs: List[Log] = []


class CRUDOperation(DBOperation, DBCarrier):
    levels: List[LEVEL] = ['memory', 'log']
    record: Schema | List[Schema]


class DBCreate(CRUDOperation):
    op_name: str = 'CREATE'


class DBRead(CRUDOperation):
    op_name: str = "READ"
    session: object
    raw: bool = False

    select: List[COLUMN] | None = None
    limit: int | None = None
    where: List[tuple] | None = None
    order: str | None = None
    record: List[Schema] | None = None
    # TODO in 1.1 group & having


class DBUpdate(CRUDOperation):
    op_name: str = "UPDATE"
    update: List[COLUMN]


class DBDelete(CRUDOperation):
    op_name: str = "DELETE"

    record: List[ID]

