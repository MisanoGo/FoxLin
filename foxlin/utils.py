from typing import Dict, List, Any

#from .philosophy import Schema : can not import


def genid(base: int):
    x = base -1
    while True:
        x = x+1
        yield x


def migrate(path, obj):
    # TODO in 1.1
    pass

def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

