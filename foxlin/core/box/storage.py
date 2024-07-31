from typing import List, Dict

import os
import orjson
import shutil

from foxlin.core.column import BaseColumn
from foxlin.core.database import (
    Schema,
    DBCarrier,
    DB_TYPE,
    LEVEL
)

from foxlin.core.operation import (
    Log,
    JsonDBOP,
    DBDump,
    DBLoad,
    CreateJsonDB,
    
    STORAGE
)

from .base import FoxBox

from foxlin.errors import InvalidDatabaseSchema

class StorageBox(FoxBox):
    """
    StorageBox is the subclass of FoxBox object
    for manage operation in json file state
    """
    file_type = '.json'
    level: LEVEL = STORAGE

    def _validate(self, data: dict, schema: Schema) -> bool:
        scl: List[str] = schema.columns  # get user definate Schema column list
        dcl: List[str] = list(data.keys())  # get raw database column
        return scl == dcl  # validate database columns with schema columns

    def _translate(self, data: Dict, db: Schema) -> Schema:
        for _column in db.columns:
            cdata = data[_column]
            column: BaseColumn = db[_column]

            column.attach(cdata)
        return db

    def _backup(self, obj: JsonDBOP):
        path = obj.path
        backup_path = path + '.backup'

        shutil.move(path, backup_path)

    def _restore(self, obj: JsonDBOP):
        path = obj.path
        backup_path = path + '.backup'

        if os.path.exists(backup_path):
            shutil.move(backup_path, path)

    def _load(self, path: str, schema: Schema) -> DB_TYPE:
        with open(path, 'r') as file:
            data = orjson.loads(file.read())['db']
            db = schema()
            if not self._validate(data, db): raise InvalidDatabaseSchema
            db = self._translate(data, db)
            return db

    def load_op(self, obj: DBLoad) -> DBCarrier:
        db = self._load(obj.path, obj.structure)
        obj.db = db
        return obj

    def _dump(self, path: str, db: Schema, mode='wb+'):
        
        columns = db.columns
        data = {
            c : db[c].data.tolist()
            for c in columns
        }
        with open(path, mode) as dbfile:
            dbfile.write(orjson.dumps({'db':data}))

    def dump_op(self, obj: DBDump):
        self._backup(obj)

        try :
            self._dump(obj.path, obj.db)
        except Exception as ex:
            self._restore(obj)

            raise ex

    def create_database_op(self, obj: CreateJsonDB):
        db = obj.structure()
        self._dump(obj.path, db, mode='xb+')  # mode set for check database dosent exists

        log = Log(box_level=self.level,
                  log_level='IN6465FO',
                  message=f'database created at {obj.path}.')
        obj.logs.append(log)
