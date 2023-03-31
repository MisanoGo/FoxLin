from collections import UserDict

class TupleGraph(UserDict):

    def __init__(self,**kwargs):
        self.bvdata = {}

        super(TupleGraph, self).__init__(**kwargs)
    
    def __getitem__(self, i):
        if i in self.data:
            return self.data[i]
        elif i in self.bvdata:
            return self.bvdata[i]
        raise KeyError(i)
    
    def __setitem__(self,k,v):
        self.data[k] = v
        if v in self.bvdata:
            self.bvdata[v].add(k)
        else :
            self.bvdata[v] = set({k})

    def __delitem__(self, key):
        v = self[key]
        v.remove(key)
        del self.data[key]
        if len(self.bvdata[v]) == 0: del self.bvdata[v]

    def __contains__(self, key):
        return key in self.data or key in self.bvdata

def tg_typer(obj):
    if isinstance(obj, TupleGraph):
        return obj.data
