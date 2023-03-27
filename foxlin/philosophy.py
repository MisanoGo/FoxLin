from abc import ABC, abstractstaticmethod
from typing import List, Dict, Union

from pydantic import BaseModel

VALID_TYPES = Union[str,int]
DB_TYPE = Dict[str ,VALID_TYPES]

class Schema(BaseModel):
    ID: int

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


