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
    record : Schema

class DBCreate(DBOperation):
    op_name: str = 'CREATE'

class DBRead(DBOperation):
    op_name: str = "READ"

class DBUpdate(DBOperation):
    op_name: str = "UPDATE"

class DBDelete(DBOperation):
    op_name: str = "DELETE"

class FileSystem(ABC):
    def __init__(self, path: str):
        raise NotImplementedError

    @abstractstaticmethod
    def load(self) -> DBCarrier:
        raise NotImplementedError

    @abstractstaticmethod
    def operate(self, obj: DBOperation):
        raise NotImplementedError


