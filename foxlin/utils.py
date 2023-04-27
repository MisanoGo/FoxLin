from typing import  Any

#from .sophy import Schema

class genid:
    def __init__(self, base: int|str):
        # handle & generate as a hex or int
        self.t = type(base)
        self.x = base if self.t is int else int(base, 16)

    def __call__(self):
        self.x += 1
        y = self.x if self.t is int else hex(self.x)
        return y

def migrate(path, new_schema):
    # TODO in 1.1
    # TODO migrate structure of changed database schema
    pass

def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

