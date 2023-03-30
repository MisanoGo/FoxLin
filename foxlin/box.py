from pathlib import Path
from typing import Callable

import orjson

import philosophy as sophy
from philosophy import *
from tog import TupleGraph

class CreateJsonDB(DBOperation):
    op_name: str = "create_database"
    base_schema: sophy.Schema = None

class DBLoad(DBOperation):
    op_name = 'LOAD'

class DBDump(DBCarrier,DBOperation):
    op_name = 'DUMP'
    
class JsonBox(FoxBox):
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
            dbfile.write(orjson.dumps(data))

    def load_op(self, obj: DBLoad) -> Any:
        data = self._load()
        return DBCarrier(db=data)

    def dump_op(self, obj: DBDump):
        self._dump({'db':obj.dict()['db']})

    def create_database_op(self,obj: CreateJsonDB):
        print(obj.base_schema)
        structuer = {
            'db' :{
                c:{}
                for c in obj.base_schema.construct().schema()['properties'].keys()
            }
        }
        self._dump(structuer)

