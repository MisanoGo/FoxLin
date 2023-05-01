from typing import List, Callable

from pydantic import BaseModel as BsMdl

from .column import BaseColumn, IDColumn
from foxlin.utils import get_attr
#from .den import Den


ID = int
COLUMN = str
LEVEL = str

class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True


class Schema(BaseModel):
    """
    databaser schema aliaser & also record container
    """
    ID: IDColumn | int = IDColumn()


    def __getitem__(self, i) -> BaseColumn:
        return self.__dict__[i]

    def __setitem__(self, name, value):
        setattr(self, name, value)

    @property
    def columns(self):
        return list(self.__dict__.keys())

DB_TYPE = Schema

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

