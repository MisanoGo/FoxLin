from typing import  Any

#from .sophy import Schema

def genid(base: int|str):
    itype = type(base)
    x = int(base, 16) if itype == str else base

    while True:
        x = x+1
        yield x if itype == int else hex(x)


def migrate(path, new_schema):
    # TODO in 1.1
    # TODO migrate structure of changed database schema
    pass

def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

