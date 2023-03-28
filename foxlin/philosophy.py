from abc import ABC, abstractstaticmethod
from typing import List, Dict, Union

from pydantic import BaseModel

ID = int
COLUMN = str
VALID_DATA_TYPES = Union[str,int]
RECORDS = Dict[ID, Union[VALID_DATA_TYPES, List[VALID_DATA_TYPES]]]
DB_TYPE = Dict[COLUMN,RECORDS]

class Schema(BaseModel):
    ID: ID

class DBCarrier(BaseModel):
    db: DB_TYPE

class DBOperation(BaseModel):
    op_name: str

class CRUDOperation(DBOperation):
    record : Schema

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
    def load(self) -> DBCarrier:
        raise NotImplementedError

    @abstractstaticmethod
    def operate(self, obj: DBOperation):
        raise NotImplementedError


