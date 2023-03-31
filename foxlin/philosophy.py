from abc import ABC, abstractstaticmethod
from typing import List, Dict, Union, Callable, Any

from pydantic import BaseModel

from tog import TupleGraph

def tg_typer(obj):
    if isinstance(obj, TupleGraph):
        return obj.data


ID = str
COLUMN = str
DB_TYPE = Dict[COLUMN,TupleGraph]

class Schema(BaseModel):
    ID: ID

class DBCarrier(BaseModel):
    db: DB_TYPE

    class Config:
        arbitrary_types_allowed = True

class DBOperation(BaseModel):
    op_name: str
    callback: Callable= None

class CRUDOperation(DBOperation):
    record : Schema = Schema

class DBCreate(CRUDOperation):
    op_name: str = 'CREATE'

class DBRead(CRUDOperation):
    op_name: str = "READ"

class DBUpdate(CRUDOperation):
    op_name: str = "UPDATE"

class DBDelete(CRUDOperation):
    op_name: str = "DELETE"

class FoxBox():
    def __init__(self, path: str):
        raise NotImplementedError

    @abstractstaticmethod
    def load_op(self) -> DBCarrier:
        raise NotImplementedError

    def operate(self,obj: DBOperation):
        operator: Callable = self.__getattribute__(obj.op_name.lower()+'_op')
        result =  operator(obj)

        return obj.callback(result) if obj.callback else result

    @abstractstaticmethod
    def read_op(self, obj: DBRead):
        pass

    @abstractstaticmethod
    def create_op(self, obj: DBCreate):
        pass

    @abstractstaticmethod
    def update_op(self, obj: DBUpdate):
        pass

    @abstractstaticmethod
    def delete_op(self, obj: DBDelete):
        pass
