import pathlib
from typing import Callable

import orjson

from philosophy import FoxBox, DBCarrier, DBOperation, DB_TYPE


class CreateJsonDB(DBOperation):
    path: str
    op_name: str = "createDatabase"
    base_schema: DBCarrier = DBCarrier(db={"ID":{0:0}})

class JsonBox(FoxBox):
    file_type = '.json'

    def __init__(self, path: str):
        self.path = pathlib.Path(path)

        if path.endswith(self.file_type):
            if self.path.exists():
                with open(path,'r') as file:
                    self.data = orjson.loads(file)

            else:
                self.operate(CreateJsonDB(path=path))

    def load(self) -> DBCarrier:
        return DBCarrier(db=self.data)

    def operate(self,obj: DBOperation):
        operator: Callable = self.__getattribute__(obj.op_name)
        return operator(obj)

    def createDatabase(self,obj: CreateJsonDB):
        with open(obj.path,'w+',encoding='utf-8') as dbfile:
            dbfile.write(obj.base_schema.json())
