from pathlib import Path
from typing import Callable

import orjson

from philosophy import *


class CreateJsonDB(DBOperation):
    op_name: str = "create_database"
    base_schema: DBCarrier = DBCarrier(db={"ID":{0:0}})

class DBLoad(DBOperation):
    op_name = 'LOAD'

class DBDump(DBCarrier,DBOperation):
    op_name = 'DUMP'
    
class JsonBox(FoxBox):
    file_type = '.json'

    def __init__(self, path: str):
        self.path = path
        if path.endswith(self.file_type):
            if not Path(path).exists():
                self.operate(CreateJsonDB(path=path))


    def _load(self):
        with open(self.path,'r') as file:
            return orjson.loads(file.read())['db']

    def _dump(self, data: Dict):
        with open(self.path,'wb+')as dbfile:
            dbfile.write(orjson.dumps(data))

    def load_op(self, obj: DBLoad) -> Any:
        data = self._load()
        return DBCarrier(db=data)

    def dump_op(self, obj: DBDump):
        self._dump({'db':obj.dict()['db']})

    def create_database_op(self,obj: CreateJsonDB):
        self._dump(obj.base_schema.dict())

