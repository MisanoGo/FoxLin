from typing import Iterable

from numpy import array, log2, concatenate, where

from foxlin.utils import genid

class FoxNone:
    __repr__ = lambda self: self.__class__.__name__
    __str__ = __repr__

    filter = lambda data: filter(lambda x: x != FoxNone ,data)

class BaseColumn:
    """
    column data manager

    here uses numpy array for contain data
    why numpy ? for auto handle queries & data managing

    <flag> is value for define max of record insertd
    uses because always just some part of array is reched
    and have a empty part

    Parameters
    ----------
    data: list
        data will initial with numpy array
    """
    def __init__(self):
        self._data = array([], dtype=object)
        self.flag  = 0


    def __grow(self):
        """ auto check to resize array """
        _data = self._data
        chunck = self.flag / _data.size * 100 # define data volume by percent
        change = -1 if chunck < 35 else +1 if chunck > 90 else 0

        if change:
            new_size = int(2**(log2(_data.size) + change))
            self.__resize(new_size)

    def attach(self, data=[]):
        xd = array(data, dtype=object)
        yd = concatenate((self.data, xd))

        self._data = yd
        # define max record index in array

        if len(self._data) < 1:
            self.__resize(8)
        else:
            self.flag = len(self._data)
        self.__grow()


    def append(self, v):
        flag = self.flag
        self[flag] = v
        return flag

    def update(self, i, v):
        self[i] = v

    def pop(self, i):
        self._data[i] = FoxNone

    def __resize(self, size):
        self._data.resize(size, refcheck=False)

    def __getitem__(self, i):
        assert i<self.flag
        return self._data[i]

    def __setitem__(self, k, v):
        self._data[k] = v
        if k >= self.flag : self.flag += 1
        self.__grow()

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self.data)})'

    __eq__ = lambda self, o: self.data == o
    __gt__ = lambda self, o: self.data >  o
    __lt__ = lambda self, o: self.data <  o
    __contains__ = lambda self, o: o in self.data

    @property
    def data(self):
        data = self._data[:self.flag]
        return data[where(data != FoxNone)]# filter None objects

class RaiColumn(BaseColumn):
    """
    Right Access Index
    is a sub class of Base Column to develop a state
    to able get value index with order(1)
    """
    def __init__(self):

        super(RaiColumn, self).__init__()

    def attach(self, data: Iterable = []):
        self.reli = {
            hash(data[i]) : i
            for i in range(len(data))
        }

        super().attach(data)

    def getv(self, v):
        return self.reli[hash(v)]

    def geti(self, i):
        return self[i]

    def __setitem__(self, k, v):
        super().__setitem__(k, v)

        self.reli[hash(v)] = k
 
    def popi(self, i):
        v = self.geti(i)
        super().pop(i)
        self.reli.pop(hash(v))

    def pop(self, i):
        # just alias for popi
        self.popi(i)

    def popv(self, v):
        i = self.getv(v)
        super().pop(i)
        self.reli.pop(hash(v))
 

class UniqeColumn(RaiColumn):
    def __init__(self):
        super(UniqeColumn, self).__init__()

    def attach(self, data: Iterable = []):
        sndata = set(data)
        s_data = set(self.data)

        assert list(sndata) == list(data) # check input data list is uniqe or not
        assert s_data | sndata == s_data ^ sndata

        super().attach(data)

    def __setitem__(self, k, v):
        assert hash(v) not in self.reli.keys()
        super().__setitem__(k, v)



class IDColumn(UniqeColumn):
    """
    implemented for ID column in schema of table

    """
    def __init__(self):
        super(IDColumn, self).__init__()

    def attach(self, data: Iterable = []):
        super().attach(data)
        self.fid = genid(self._data[self.flag-1])

    def plus(self):
        _id = self.fid()
        return self.append(_id)


class Column(BaseColumn):
    # Just alias of BaseColumn
    pass