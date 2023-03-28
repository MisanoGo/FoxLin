from pathlib import Path
from typing import Callable

import orjson

from philosophy import *


class CreateJsonDB(DBOperation):
    path: str
    op_name: str = "create_database"
    base_schema: DBCarrier = DBCarrier(db={"ID":{0:0}})

class DBLoad(DBOperation):
    op_name = 'LOAD'

class JsonBox(FoxBox):
    file_type = '.json'

    def __init__(self, path: str):
        self.path = path
        if path.endswith(self.file_type):
            if not Path(path).exists():
                self.operate(CreateJsonDB(path=path))


    def _load(self, path):
        with open(path,'r') as file:
            return orjson.loads(file.read())['db']

    def load_op(self, obj: DBLoad) -> Any:
        self.data = self._load(self.path)
        return obj.callback.func(DBCarrier(db=self.data))

    def create_database_op(self,obj: CreateJsonDB):
        with open(obj.path,'w+',encoding='utf-8') as dbfile:
            dbfile.write(obj.base_schema.json())

    def read_op(self, obj: DBRead):
        pass

    def create_op(self, obj: DBCreate):
        pass

    def update_op(self, obj: DBUpdate):
        pass

    def delete_op(self, obj: DBDelete):
        pass
