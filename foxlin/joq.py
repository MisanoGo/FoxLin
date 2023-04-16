
"""
Joq.py used for Dbms queries
every dbms queries will write in JsonQuery object as methods
using by: query = JsonQuery()
          query.<query_method_name>()
"""

from numpy import where, argsort, copy
from random import choice

class JsonQuery(object):
    def __init__(self, session):
        self.session = session
        self.records = []
        self.__state = None
        self.reset()

    def reset(self):
        ID_column = self.session._db['ID']
        self.records = copy(ID_column.values()[:ID_column.flag])

    def first(self):
        return self.session.get_by_id(self.records[0])

    def end(self):
        return self.session.get_by_id(self.records[-1])

    def rand(self):
        rand_id = choice(self.records)
        return self.session.get_by_id(rand_id)

    def all(self):
        # bug : after reload record 0 exists
        for ID in self.records:
            yield self.session.get_by_id(ID)
        self.reset()

    def SELECT(self, *args, **kwargs):
        return self

    def WHERE(self, condition):
        self.records = self.session._db[self.__state].k_array[where(condition)]
        return self

    def ORDER_BY(self, order_column):
        self.records = self.records[argsort(getattr(self, order_column)[:self.session._db['ID'].flag])]
        return self

    def GROUP_BY(self, *args, **kwargs):
        return self

    def HAVING(self, *args, **kwargs):
        return self

    def LIMIT(self, n: int):
        self.records = self.records[:n]
        return self

    def __getattribute__(self, name):
        session = object.__getattribute__(self,'session')
        if name in session._db.keys():
            self.__state = name
            return self.session._db[name].values()[:self.session._db['ID'].flag]
        return object.__getattribute__(self, name)
