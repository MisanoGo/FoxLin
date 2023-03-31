from pathlib import Path
from typing import Callable

import orjson

from philosophy import *
from tog import TupleGraph
from utils import getStructher

class FoxBox():
    """
    Foxbox is a operate manager for CRUD and user-self operator definated
    can use in states of memory-cache database and file-based db
    """
    def __init__(self):
        raise NotImplementedError

    @abstractstaticmethod
    def load_op(self) -> DBCarrier:
        raise NotImplementedError

    def operate(self,obj: DBOperation):
        operator: Callable = self.__getattribute__(obj.op_name.lower()+'_op')
        result =  operator(obj)

        return obj.callback(result) if obj.callback else result

    @abstractstaticmethod
    def read_op(self, obj: DBRead):
        pass

    @abstractstaticmethod
    def create_op(self, obj: DBCreate):
        pass

    @abstractstaticmethod
    def update_op(self, obj: DBUpdate):
        pass

    @abstractstaticmethod
    def delete_op(self, obj: DBDelete):
        pass


class CreateJsonDB(DBOperation):
    op_name: str = "create_database"
    base_schema: Schema = None

class DBLoad(DBOperation):
    op_name = 'LOAD'

class DBDump(DBCarrier,DBOperation):
    op_name = 'DUMP'
    
class JsonBox(FoxBox):
    """
    JsonBox is the subclass of FoxBox object for manage operation in json file state
    """
    file_type = '.json'

    def __init__(self, path: str, schema: Schema):
        self.path = path
        if path.endswith(self.file_type):
            if not Path(path).exists():
                so = CreateJsonDB()
                so.base_schema = schema
                self.operate(so)

    def _translate(self,data: DB_TYPE):
        data_n = {c:TupleGraph(**r) for c,r in data.items()}
        return data_n

    def _load(self):
        with open(self.path,'r') as file:
            return self._translate(orjson.loads(file.read())['db'])

    def _dump(self, data: Dict):
        with open(self.path,'wb+')as dbfile:
            dbfile.write(orjson.dumps(data,default=tg_typer))

    def load_op(self, obj: DBLoad) -> Any:
        data = self._load()
        return DBCarrier(db=data)

    def dump_op(self, obj: DBDump):
        self._dump({'db':obj.dict()['db']})

    def create_database_op(self,obj: CreateJsonDB):
        self._dump({'db':getStructher(obj.base_schema)})

