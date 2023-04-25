
"""
Joq.py used for Dbms queries
every dbms queries will write in JsonQuery object as methods
using by: query = JsonQuery()
          query.<query_method_name>()
"""
from typing_extensions import Self
from typing import Generator, Callable

from numpy import where, argsort, array, argwhere, arange
from random import choice

from .sophy import Schema
from .column import Column, FoxNone
from .utils import get_attr 

class JsonQuery(object):
    def __init__(self, session):
        self.session = session
        self.records = []
        self.selected_col = set()
        self.raw = False

        self.reset()

    @property
    def __get_records(self):
        return arange(len(self.ID))

    def reset(self):
        self.records = self.__get_records
        self.selected_col = set()

    def get_one(self, ID: int):
        return self.session.get_one(ID, columns=self.selected_col, raw=self.raw)

    def get_many(self, *ID: int):
        return self.session.get_many(*ID,columns=self.selected_col, raw=self.raw)

    def first(self):
        return self.get_one(self.rcords[0])

    def end(self):
        return self.get_one(self.records[-1])

    def rand(self):
        rand_id = choice(self.records)
        return self.get_one(rand_id)

    def all(self) -> Generator:
        return self.get_many(*self.records)
        self.reset()

    def select(self,*column: str) -> Self:
        self.selected_col = set(column)
        return self

    def where(self, *condition) -> Self:
        recset = set(self.records)
        recs = self.__get_records

        for con in condition:
            x = recs[argwhere(con)]
            y = x.reshape(len(x))
            recset = recset & set(y)
        self.records = array(list(recset))
        return self

    def order_by(self, column: Column) -> Self:
        recs = column[self.records] # get filterd recors column data 
        sorted_recs_index = argsort(recs) # sort them & return index's
        self.records = self.records[sorted_recs_index] # sort ID data by sorted column data args
        return self

    def group_by(self, *args, **kwargs) -> Self:
        # TODO in 1.1
        return self

    def having(self, *args, **kwargs) -> Self:
        # TODO in 1.1
        return self

    def limit(self, n: int) -> Self:
        self.records = self.records[:n]
        return self

    def count(self):
        return len(self.records)

    def filter(self, func: Callable[[Schema], bool]) -> filter:
        return filter(func, self.all())

    def rai(self, **exp):
        # TODO
        # uses for get records by column set as a right access index type
        pass

    def __getattribute__(self, name):
        try:
            return get_attr(self, name)
        except:
            # implemented for quick access of column data like : query.<column name>
            _db = self.session._db
            assert name in _db.columns # TODO : set exception # assert if column don't exists
            column = _db[name].data # get raw data
            return column[where(column != FoxNone)] # filter None objects

