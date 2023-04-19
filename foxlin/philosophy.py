from typing import List, Dict, Union, Callable

from pydantic import BaseModel as BsMdl
from numpy import ndarray, array, log2

from .utils import get_attr
#from .den import Den


ID = str
COLUMN = str
LEVEL = str

class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True

class Column:
    def __init__(self, data = []):
        self.data = array(data, dtype=object)
        flag = len(data)
        if flag == 0 : 
            self.__resize(8)
        
        self.flag = len(self.data) if flag else len(data)
        self.__grow()

        #if self.right :
        #    self.relation = {}
 
    def __grow(self):
        chunck = self.flag / self.data.size * 100
        change = -1 if chunck < 35 else +1 if chunck > 90 else 0
        if change:
            new_size = int(2**(log2(self.data.size) + change))
            self.__resize(new_size)

    def append(self, v):
        self[self.flag] = v

    def update(self, i, v):
        self[i] = v

    def pop(self, i):
        self.data.pop(i)

    def __resize(self, size):
        self.data.resize(size, refcheck=False)

    def __getitem__(self, i):
        return self.data[:self.flag][i]

    def __setitem__(self, k, v):
        self.data[k] = v
        if k >= self.flag : self.flag += 1
        self.__grow()

    def __iter__(self):
        return iter(self.ldata)

class Schema(BaseModel):
    """
    databaser schema aliaser & also record container
    """

    def __getitem__(self, i):
        return get_attr(self, i)

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

