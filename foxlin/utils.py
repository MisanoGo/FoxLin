from typing import Dict, List, Any

from .philosophy import Schema

def migrate(path, obj: Schema):
    # TODO in 1.1
    pass

def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

def getKeyList(obj: Schema) -> List[str]:
    return obj.construct().schema()['properties'].keys()

def getStructher(obj: Schema, k=dict()) -> Dict[str, Any]:
    structuer = {c: k for c in getKeyList(obj)}
    return structuer
