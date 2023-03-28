from abc import ABC, abstractstaticmethod
from typing import List, Dict, Union, Callable, Any

from pydantic import BaseModel

ID = int
COLUMN = str
VALID_DATA_TYPES = Union[str,int]
RECORDS = Dict[ID, Union[VALID_DATA_TYPES, List[VALID_DATA_TYPES]]]
DB_TYPE = Dict[COLUMN,RECORDS]

class Schema(BaseModel):
    ID: ID

class OperatorCarrier(BaseModel):
    func: Callable
    args: Any

class DBCarrier(BaseModel):
    db: DB_TYPE

class DBOperation(BaseModel):
    op_name: str
    callback: OperatorCarrier = None

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

class FoxBox(ABC):
    def __init__(self, path: str):
        raise NotImplementedError

    @abstractstaticmethod
    def load_op(self) -> DBCarrier:
        raise NotImplementedError

    def operate(self,obj: DBOperation):
        operator: Callable = self.__getattribute__(obj.op_name.lower()+'_op')
        return operator(obj)

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
