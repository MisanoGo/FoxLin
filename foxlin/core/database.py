from typing import List, Callable
from typing import NewType

from .column import BaseColumn, IDColumn
from .utils import BaseModel, get_attr

ID = NewType('ID', int)
COLUMN = NewType('COLUMN', str)
LEVEL = NewType('LEVEL', str)

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



