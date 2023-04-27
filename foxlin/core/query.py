from typing_extensions import Self
from typing import Generator, Callable, Dict

from numpy import where, argsort, array, argwhere, arange
from random import choice

from .sophy import Schema
from .column import Column, FoxNone
from .utils import get_attr

class FoxQuery(object):
    """ 
    FoxQuery is a interface for operate queries of DB on memory
    in every inctance FoxQuery will get indecies of recs on ID column
    and after filter them by user through where() method
    can access filterd records by all() method or first(), end(), rand()
    also can use raw param to get raw-dict data of record

    Parameters
    ----------
    session: Den
        for access to data of columns
    """
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

    def get_by_id(self, ID: int|str) -> Schema | Dict:
        _id = self.session._db['ID'].getv(ID)
        return self.get_one(_id)

    def get_one(self, ID: int) -> Schema | Dict:
        # here ID mean index of ID in ID column
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
        # get count value of filterd records
        return len(self.records)

    def max(self, column):
        # get max value of filterd records
        return column[self.records].max() # get max of filterd records

    def min(self, column):
        # get min value of filterd records
        return column[self.records].min()

    def mean(self, column):
        # get average value of filterd records
        return column[self.records].mean()

    def filter(self, func: Callable[[Schema], bool]) -> Self:
        """ TODO """
        f = filter(func, self.all())
        self.records = array(list(f))
        return self

    def rai(self, **exp):
        # TODO in 1.1
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

