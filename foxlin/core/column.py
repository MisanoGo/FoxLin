from typing import Iterable, Any

from numpy import array, concatenate, arange, roll

from foxlin.utils import genid


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
    dtype: Any
        define for type checking & less memory usage
    """
    def __init__(self, dtype: Any=object, default=None):
        self.data = array([], dtype=dtype)
        self.default = default
        self.dtype = dtype


    def attach(self, data=[]):
        # use for multi data 
        xd = array(data, dtype=self.dtype)
        yd = concatenate((self.data, xd))

        self.data = yd

    def append(self, v=None):
        v = v if v else self.default # set default value if v is None

        flag = self.flag
        self[flag] = v
        return flag

    def update(self, i, v):
        self[i] = v

    def pop(self, i):
        data = self.data
        size = self.data.size

        # send specified item to end of array
        data = array(roll(data, size-i)[::-1])
        data.resize(size-1, refcheck=False) # remove lase item
        data = array(roll(data, size-i-1)[::-1])# reset array
        self.data = data

    def __resize(self, size):
        self.data.resize(size, refcheck=False)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, k, v):
        if k >= self.flag :
            self.__resize(self.flag+1)

        self.data[k] = v

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self.data)})'

    __eq__ = lambda self, o: self.data == o
    __gt__ = lambda self, o: self.data >  o
    __lt__ = lambda self, o: self.data <  o
    __contains__ = lambda self, o: o in self.data

    @property
    def flag(self):
        return self.data.size


class RaiColumn(BaseColumn):
    """
    Right Access Index
    is a sub class of Base Column to develop a state
    to able get value index with order(1)
    """
    def __init__(self, dtype: Any=object, default=None):
        super(RaiColumn, self).__init__(dtype, default)
        self.reli = {

        }

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

    @property
    def davat(self):
        return self._data[list(self.reli.values())]
 

class UniqeColumn(RaiColumn):
    def __init__(self, dtype: Any=object, default=None):
        super(UniqeColumn, self).__init__(dtype, default)

    def attach(self, data: Iterable = []):
        sndata = set(data)
        s_data = set(self.data)

        assert sorted(sndata) == sorted(data) # check input data list is uniqe or not
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
        self.fid = genid(self._flagid)

    def plus(self):
        _id = self.fid()
        return self.append(_id)

    def parange(self, length: int):
        par = arange(self._flagid+1, length)
        self.attach(par)

    @property
    def _flagid(self):
        return self.data[self.flag-1] if self.flag != 0 else 0






def column(uniqe: bool=False, rai:bool=False, dtype: Any=object, default=None):
    """
    Column Factory function

    Parameters
    ----------
    uniqe: bool

    """
    kwargs = {
        'dtype':dtype,
        'default':default
    }

    if uniqe:
        return UniqeColumn(**kwargs)
    if rai:
        return RaiColumn(**kwargs)

    return BaseColumn(**kwargs)

