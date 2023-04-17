from typing import Dict, List, Any

#from .philosophy import Schema : can not import

def migrate(path, obj):
    # TODO in 1.1
    pass

def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

def getKeyList(obj) -> List[str]:
    return obj.construct().schema()['properties'].keys()

def getStructher(obj, k=dict()) -> Dict[str, Any]:
    structuer = {c: k for c in getKeyList(obj)}
    return structuer
