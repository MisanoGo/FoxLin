from typing import Iterable

from numpy import array, log2

from foxlin.utils import genid

class FoxNone:
    __repr__ = lambda self: self.__class__.__name__
    __str__ = __repr__

    filter = lambda data: filter(lambda x: x != FoxNone ,data)

class BaseColumn:
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
        self.flag = len(self._data) if flag else len(data) # max inserted arg
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
        self._data[i] = FoxNone

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

class RaiColumn(BaseColumn):
    """
    Right Access Index
    is a sub class of Base Column to develop a state 
    to able get value index with order(1)
    """
    def __init__(self, data: Iterable = []):
        self.reli = {
            hash(data[i]) : i
            for i in range(len(data))
        }

        super(RaiColumn, self).__init__(data)

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
    def __init__(self, data: Iterable = []):
        assert list(set(data)) == list(data) # check input data list is uniqe or not

        super(UniqeColumn, self).__init__(data)

    def __setitem__(self, k, v):
        assert hash(v) not in self.reli.keys()
        super().__setitem__(k, v)



class IDColumn(UniqeColumn):
    def __init__(self, data: Iterable = []):
        super(IDColumn, self).__init__(data)

        self.fid = genid(self._data[self.flag-1])

    def plus(self):
        _id = next(self.fid)
        return self.append(_id)


class Column(BaseColumn):
    pass
