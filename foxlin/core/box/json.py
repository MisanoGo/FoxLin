from typing import List, Dict

import orjson

from foxlin.core.column import Column, IDColumn, FoxNone
from foxlin.core.sophy import (
    Schema,
    DBOperation,
    DBCarrier,

    Log,

    DB_TYPE,
    LEVEL
)

from .fox import FoxBox



class JsonDBOP(DBOperation):
    path: str
    levels: List[LEVEL] = ['jsonfile', 'log']
    structure: Schema | None = None

    # TODO : validate path exists with pydantic validator

class CreateJsonDB(JsonDBOP):
    op_name: str = "create_database"

class DBLoad(DBCarrier, JsonDBOP):
    op_name = 'LOAD'

class DBDump(DBCarrier, JsonDBOP):
    op_name = 'DUMP'


class JsonBox(FoxBox):
    """
    JsonBox is the subclass of FoxBox object
    for manage operation in json file state
    """
    file_type = '.json'
    level: str = 'jsonfile'

    def _validate(self, data: dict, schema: Schema) -> bool:
        scl: List[str] = schema.columns  # get user definate Schema column list
        dcl: List[str] = list(data.keys())  # get raw database column
        return scl == dcl  # validate database columns with schema columns

    def _translate(self, data: Dict, db: Schema) -> Schema:
        for _column in db.columns:
            cdata  = data[_column]
            column = db[_column]

            column.attach(cdata)
        return db

    def _load(self, path: str, schema: Schema) -> DB_TYPE:
        with open(path, 'r') as file:
            data = orjson.loads(file.read())['db']
            db = schema()
            if self._validate(data, db):
                db = self._translate(data, db)
                return db
            raise ValueError

    def load_op(self, obj: DBLoad) -> DBCarrier:
        db = self._load(obj.path, obj.structure)
        obj.db = db
        return obj

    def _dump(self, path: str, db: Schema, mode='wb+'):
        columns = db.columns
        data = {
            c : list(FoxNone.filter(db[c].data))
            for c in columns
        }
        with open(path, mode) as dbfile:
            dbfile.write(orjson.dumps({'db':data}))

    def dump_op(self, obj: DBDump):
        db = obj.db
        self._dump(obj.path, db)

    def create_database_op(self, obj: CreateJsonDB):
        db = obj.structure()
        self._dump(obj.path, db, mode='xb+')  # mode set for check database dosent exists

        log = Log(box_level=self.level,
                  log_level='INFO',
                  message=f'database created at {obj.path}.')
        obj.logs.append(log)

