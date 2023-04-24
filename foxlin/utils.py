from typing import Dict, List, Any

#from .philosophy import Schema : can not import


def genid(base: int|str):
    itype = type(base)
    x = int(base, 16) if itype == str else base

    while True:
        x = x+1
        yield x if itype == int else hex(x)


def migrate(path, obj):
    # TODO in 1.1
    pass

def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

