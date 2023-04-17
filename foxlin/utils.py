from .philosophy import Schema

def migrate(path, obj: Schema):
    # TODO in 1.1
    pass

def get_attr(obj, name):
    return object.__getattribute__(obj, name)

def getKeyList(obj: Schema):
    return obj.construct().schema()['properties'].keys()

def getStructher(obj: Schema, k=dict()):
    structuer = {c: k for c in getKeyList(obj)}
    return structuer
