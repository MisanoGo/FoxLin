import numpy as np

from typing import List, Dict, Any, Iterable, Hashable, Tuple



class TupleGraph:
    """
    TupleGraph is new implementation from dict data structure as graph
    why graph ? because you can accsess from key to value and from value to key
    k,v must be Hashable & whene v be list it will convert to tuple

    >>> d = {'id':195, 'name':'tommy'}
    >>> tg = TupleGraph(d)
    >>> tg['name']
    <<< 'tommy'
    >>> tg[:195]
    <<< 'id'

    >>> tg = TupleGraph(d, uniqe=True)
    <<< tg['username'] = 'tommy' # raise error

    """
    def __init__(self, data: dict = None, space: int=8, default=None, uniqe: bool=False):
        self.k_array = np.empty(space, dtype=object)
        self.v_array = np.empty(space, dtype=object)

        self.uniqe = uniqe
        self.default = default
        
        self.__flag = 0
        self.relation: Dict[str,Dict[int,Any]] = {'k':{},
                                                  'v':{}}
        self.update(data)

    def __getitem__(self, i):
        if type(i) is slice:
            if i.stop:
                return self.__get_by_v(i.stop)
            elif i.start:
                return self.__get_by_k(i.start)
        elif type(i) is tuple:
            return [self.__get_by_k(k) for k in i]
        else:
            return self.__get_by_k(i)

    def __setitem__(self, k: Hashable, v: Hashable):
        if type(v) is list:
            v = tuple(v)
        if type(k) is slice:
            pass
        elif type(k) is Iterable:
            pass
        else :
            self.__set_i(k, v)


    def __resize(self, new_size: int):
        self.k_array.resize(new_size, refcheck=False)
        self.v_array.resize(new_size, refcheck=False)

    def _grow(self):
        chunck = self.__flag / self.k_array.size * 100
        change = -1 if chunck < 35 else +1 if chunck > 90 else 0
        if change:
            new_size = int(2**(np.log2(self.k_array.size) + change))
            self.__resize(new_size)

    def __set_i(self, k, v):
        k_exist = k in self
        v_exist = v in self.v_array
        if self.uniqe:
            if v_exist :
                raise Exception # split def 
        flag = self.__flag
        self.k_array[flag]= k
        self.v_array[flag]= v
        
        self.relation['k'][hash(k)] = flag
        if not self.uniqe:
            flag: List[int] = [flag,*self.relation['v'][hash(v)]] if v_exist else [flag]
        self.relation['v'][hash(v)] = flag

        if not k_exist: self.__flag += 1
        self._grow()

    def __get_by_i(self, p, i) -> int | List[int]:
        return self.relation[p][hash(i)]

    def __get_by_k(self, k):
        flag = self.__get_by_i('k', k)
        return self.v_array[flag]

    def __get_by_v(self, v):
        flag = self.__get_by_i('v', v)
        return self.k_array[flag]

    def __contains__(self, key) -> bool:
        return key in self.k_array


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
        self.k_array.fill(None)
        self.v_array.fill(self.default)
        self.__flag = 0
        self._grow()

    def get(self, *key) -> Hashable:
        return self[key]

    def keys(self):
        return self.k_array

    def values(self):
        return self.v_array

    def items(self) -> List[Tuple[Hashable, Hashable]]:
        return tg_typer(self).items()

    def update(self, data: Dict[Hashable, Hashable]):
        tuple(map(lambda i: self.__setitem__(i[0],i[1]),data.items()))

    def __repr__(self):
        return f"{self.__class__.__name__} : ({str(tg_typer(self))})"

    @property
    def flag(self):
        return self.__flag

def tg_typer(obj) -> Dict | None:
    if isinstance(obj, TupleGraph) :
        data = {str(k):v
                for k,v in zip(obj.k_array[:obj.flag],
                               obj.v_array[:obj.flag])}
        if '0' in data:
            data.pop('0')
        if 'None' in data:
            data.pop('None')
        return data

