from pathlib import Path
from typing import Callable

import orjson

from philosophy import *
from tog import TupleGraph
from utils import getStructher


class FoxBox:
    """
    Foxbox is a operate manager for CRUD and user-self operator definated
    can use in states of memory-cache database and file-based db

    dbom: database operation manager
    """
    parent= None
    level: str = 'set level of operation'

    def __init__(self, parent = None):
        self.parent = parent

    def operate(self,obj: DBOperation):
        if isinstance(obj, DBOperation):
            if self.level in obj.levels:
                operator: Callable = self.__getattribute__(obj.op_name.lower()+'_op')
                result =  operator(obj)

                if obj.callback_level == self.level:
                    obj.callback(result) if obj.callback else result

            if self.parent: # check for parent dbom exists
                self.parent.operate(obj) # send operation to parent class


class MemBox(FoxBox):
    level: str = 'memory'

    def create_op(self, obj: DBCreate):
        pass

    def read_op(self, obj: DBRead):
        pass

    def update_op(self, obj: DBUpdate):
        pass

    def delete_op(self, obj: DBUpdate):
        pass



class CreateJsonDB(DBOperation):
    op_name: str = "create_database"
    
    base_schema: Schema = None

class DBLoad(DBOperation):
    op_name = 'LOAD'
    path: str = ''

class DBDump(DBCarrier,DBOperation):
    op_name = 'DUMP'
    path: str = ''

class JsonBox(FoxBox):
    """
    JsonBox is the subclass of FoxBox object for manage operation in json file state
    """
    file_type = '.json'
    level: str = 'jsonfile'

    def _translate(self,data: DB_TYPE):
        data_n = {c:TupleGraph(**r) for c,r in data.items()}
        return data_n

    def _load(self, path: str):
        with open(path,'r') as file:
            return self._translate(orjson.loads(file.read())['db'])

    def _dump(self,path: str, data: Dict, mode='wb+'):
        with open(path, mode) as dbfile:
            dbfile.write(orjson.dumps(data,default=tg_typer))

    def load_op(self, obj: DBLoad) -> Any:
        data = self._load(obj.path)
        return DBCarrier(db=data)

    def dump_op(self, obj: DBDump):
        self._dump(obj.path,{'db':obj.dict()['db']})

    def create_database_op(self,obj: CreateJsonDB):
        self._dump(obj.path,{'db':getStructher(obj.base_schema)},mode='xb+') # mode set for check database dosent exists

class LogBox(FoxBox):
    level: str = 'log'

    def operate(self, obj: DBOperation):
        for i in obj.logs:
            print(i.level,i.message)

