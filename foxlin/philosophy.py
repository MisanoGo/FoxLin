from abc import ABC, abstractstaticmethod
from typing import List, Dict, Union, Callable, Any

from pydantic import BaseModel

from tog import TupleGraph


ID = str
COLUMN = str
LEVEL = str
DB_TYPE = Dict[COLUMN,TupleGraph]

class BaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class Schema(BaseModel):
    """
    databaser schema aliaser & also record carrier
    """
    ID: ID

class DBCarrier(BaseModel):
    db: DB_TYPE = None

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
    callback: Callable = None
    callback_level: LEVEL = None# that level callback can call

    levels: List[LEVEL] = ['log']
    logs: List[Log] = []


class CRUDOperation(DBOperation, DBCarrier):
    levels: List[LEVEL] = ['memory','log']
    record : Schema

class DBCreate(CRUDOperation):
    op_name: str = 'CREATE'

class DBRead(CRUDOperation):
    op_name: str = "READ"

class DBUpdate(CRUDOperation):
    op_name: str = "UPDATE"
    updated_fields: List[str]

class DBDelete(CRUDOperation):
    op_name: str = "DELETE"


