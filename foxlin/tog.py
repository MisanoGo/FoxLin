import numpy as np

from typing import Dict, Any, Iterable


class TupleGraph:

    def __init__(self, space: int=8, default=None, grow: bool=True):
        self.k_array = np.zeros(space, dtype=np.int64)
        self.v_array = np.zeros(space, dtype=object)

        self.default = default
        self.__flag = 0
        self.__grow = grow
        self.relation: Dict[str,Dict[int,Any]] = {'k':{},
                                                  'v':{}}

    def __getitem__(self, i):
        if type(i) is slice:
            if i.stop:
                return self.__get_by_v(i.stop)
            elif i.start:
                return self.__get_by_k(i.start)
        elif i in self:
            return self.__get_by_v(i)

    def __setitem__(self, k, v):
        if type(k) is slice:
            pass
        elif type(k) is Iterable:
            pass
        else :
            self.__set_i(k, v)

        self.__flag += 1
        if self.__grow: self._grow()

    def __resize(self, new_size: int):
        self.k_array.resize(new_size)
        self.v_array.resize(new_size)

    def _grow(self):
        chunck = self.__flag / self.k_array.size * 100
        change = -1 if chunck < 35 else +1 if chunck > 90 else 0
        if change:
            new_size = int(2**(np.log2(self.k_array.size) + change))
            self.__resize(new_size)

    def __set_i(self, k, v):
        self.k_array[self.__flag]= k
        self.v_array[self.__flag]= v

        self.relation['k'][hash(k)] = self.__flag
        self.relation['v'][hash(v)] = self.__flag

    def __get_by_i(self, p, i):
        return self.relation[p][hash(i)]

    def __get_by_k(self, k):
        flag = self.__get_by_i('k', k)
        return self.v_array[flag]

    def __get_by_v(self, v):
        flag = self.__get_by_i('v', v)
        return self.k_array[flag]

    def __contains__(self, key):
        return key in self.v_array

    def pop(self, key):
        # INFO TODO : flag -=1 if key is in last of array
        index = self.relation['k'][hash(key)]
        value = self.v_array[index]

        self.relation['k'].pop(hash(key))
        self.relation['v'].pop(hash(value))

        self.k_array[index] = 0
        self.v_array[index] = self.default

    def popitem(self):
        index = self.__flag -1
        k,v = self.k_array[index], self.v_array[index]
        self.pop(k)

        self.__flag -= 1
        return k,v

    def clear(self):
        self.relation = {'k':{},
                         'v':{}}
        self.k_array.fill(0)
        self.v_array.fill(self.default)
        self.__flag = 0
        self._grow()

    def keys(self):
        return self.k_array

    def values(self):
        return self.v_array

    def items(self):
        return set(zip(self.keys, self.values))

    def update(self, data: dict):
        # BUG : same update set up flag
        tuple(map(lambda i: self.__setitem__(i[0],i[1]),data.items()))

def tg_typer(obj):
    if isinstance(obj, TupleGraph):
        return {k:v for k,v in zip(obj.k_array, obj.v_array)}
