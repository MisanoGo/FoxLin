
"""
Joq.py used for Dbms queries
every dbms queries will write in JsonQuery object as methods
using by: query = JsonQuery()
          query.<query_method_name>()
"""
from typing_extensions import Self
from typing import Generator

from numpy import where, argsort, copy, array
from random import choice

from .philosophy import DBRead
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
        ID_column = self.session._db['ID']
        x = list(ID_column.relation['k'].values()) # only get exists index's not None or 0 as Deleted
        return copy(ID_column.values()[x])


    def reset(self):
        self.records = self.__get_records
        self.selected_col = set()

    def get(self, ID: str):
        return self.session.get_by_id(ID, self.selected_col, self.raw)

    def first(self):
        return self.get(self.records[0])

    def end(self):
        return self.get(self.records[-1])

    def rand(self):
        rand_id = choice(self.records)
        return self.get(rand_id)

    def all(self) -> Generator:
        for ID in self.records:
            yield self.get(ID)
        self.reset()

    def SELECT(self,*column) -> Self:
        self.selected_col = set(column)
        return self

    def WHERE(self, *condition) -> Self:
        recset = set(self.records)
        recs = self.__get_records
        for con in condition:
            recset = recset & set(recs[where(con)])
        self.records = array(list(recset))
        return self

    def ORDER_BY(self, column) -> Self:
        recs = self.session._db[column].get(*self.records)
        sorted_recs_index = argsort(recs)
        self.records = self.records[sorted_recs_index]
        return self

    def GROUP_BY(self, *args, **kwargs) -> Self:
        # TODO in 1.1
        return self

    def HAVING(self, *args, **kwargs) -> Self:
        # TODO in 1.1
        return self

    def LIMIT(self, n: int) -> Self:
        self.records = self.records[:n]
        return self

    def COUNT(self):
        return len(self.records)

    def rad(self, **columns): # right access data
        for k,v in columns.items():
            c = getattr(self, k)
            self.WHERE(c == v)
        d = self.first()
        self.reset()
        return d

    def liner(self, **columns):
        # liner search TODO in 1.2
        pass

    def __getattribute__(self, name):
        try:
            return get_attr(self, name)
        except:
            _db = self.session._db
            assert name in _db.keys() # TODO : set exception
            return _db[name].values()[:_db['ID'].flag]

