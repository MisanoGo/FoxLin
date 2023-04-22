from typing import List, Dict, Union, Callable, Iterable

from pydantic import BaseModel as BsMdl
from numpy import ndarray, array, log2

from .utils import genid, get_attr
#from .den import Den


ID = int
COLUMN = str
LEVEL = str

class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True

class Column:
    """
    record manager
    """
    def __init__(self, data = []):
        self._data = array(data, dtype=object)
        flag = len(data)
        if flag == 0 : 
            # if data list is empty resize array to 8 index
            self.__resize(8) 

        # define max record index in array
        self.flag = len(self._data) if flag else len(data)
        self.__grow()
 
    def __grow(self):
        """ auto check to resize array"""
        _data = self._data
        chunck = self.flag / _data.size * 100 # define data volume by percent
        change = -1 if chunck < 35 else +1 if chunck > 90 else 0

        if change:
            new_size = int(2**(log2(_data.size) + change))
            self.__resize(new_size)

    def append(self, v):
        flag = self.flag
        self[flag] = v
        return flag

    def update(self, i, v):
        self[i] = v

    def pop(self, i):
        self.data[i] = None

    def __resize(self, size):
        self._data.resize(size, refcheck=False)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, k, v):
        self._data[k] = v
        if k >= self.flag : self.flag += 1
        self.__grow()

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self.data)})'

    @property
    def data(self):
        return self._data[:self.flag]


class UniqeColumn(Column):
    def __init__(self, data: Iterable = []):
        assert list(set(data)) == list(data) # check input data list is uniqe or not

        super(UniqeColumn, self).__init__(data)

    def __setitem__(self, k, v):
        assert v not in self.data 
        super().__setitem__(k, v)

class RAIColumn(Column):
    pass

class IDColumn(RAIColumn, UniqeColumn):
    def __init__(self, data: Iterable = []):
        super(IDColumn, self).__init__(data)

        self.fid = genid(self.flag)

    def plus(self):
        _id = next(self.fid)
        return self.append(_id)


class Schema(BaseModel):
    """
    databaser schema aliaser & also record container
    """
    ID: IDColumn | int = Column()

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

