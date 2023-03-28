import pathlib
from typing import Callable

import orjson

from philosophy import *


class CreateJsonDB(DBOperation):
    path: str
    op_name: str = "create_database"
    base_schema: DBCarrier = DBCarrier(db={"ID":{0:0}})

class JsonBox(FoxBox):
    file_type = '.json'

    def __init__(self, path: str):
        self.path = pathlib.Path(path)

        if path.endswith(self.file_type):
            if not self.path.exists():
                self.operate(CreateJsonDB(path=path))
            self.data = self._load(path)

    def _load(self, path):
        with open(path,'r') as file:
            return orjson.loads(file.read())['db']

    def load(self) -> DBCarrier:
        return DBCarrier(db=self.data)

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
