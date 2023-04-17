
"""
Joq.py used for Dbms queries
every dbms queries will write in JsonQuery object as methods
using by: query = JsonQuery()
          query.<query_method_name>()
"""

from numpy import where, argsort, copy
from random import choice

from .utils import get_attr

class JsonQuery(object):
    def __init__(self, session):
        self.session = session
        self.records = []
        self.__state = None
        self.reset()

    def reset(self):
        ID_column = self.session._db['ID']
        x = list(ID_column.relation['k'].values()) # only get exists index's not None or 0 as Deleted
        self.records = copy(ID_column.values()[x])

    def first(self):
        return self.session.get_by_id(self.records[0])

    def end(self):
        return self.session.get_by_id(self.records[-1])

    def rand(self):
        rand_id = choice(self.records)
        return self.session.get_by_id(rand_id)

    def all(self):
        for ID in self.records:
            yield self.session.get_by_id(ID)
        self.reset()

    def SELECT(self, *args, **kwargs):
        return self

    def WHERE(self, condition):
        self.records = self.session._db[self.__state].k_array[where(condition)]
        return self

    def ORDER_BY(self, column):
        recs = self.session._db[column].get(*self.records)
        sorted_recs = argsort(recs)
        self.records = self.records[sorted_recs]
        return self

    def GROUP_BY(self, *args, **kwargs):
        # TODO in 1.1
        return self

    def HAVING(self, *args, **kwargs):
        # TODO in 1.1
        return self

    def LIMIT(self, n: int):
        self.records = self.records[:n]
        return self

    def __getattribute__(self, name):
        session = get_attr(self,'session')
        if name in session._db.keys():
            self.__state = name
            return self.session._db[name].values()[:self.session._db['ID'].flag]
        return get_attr(self, name)
