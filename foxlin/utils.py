from pydantic import BaseModel


def get_attr(obj, name):
    return object.__getattribute__(obj, name)

def getKeyList(obj: BaseModel):
    return obj.construct().schema()['properties'].keys()

def getStructher(obj: BaseModel, k=dict()):
    structuer = {c: k for c in getKeyList(obj)}
    return structuer
