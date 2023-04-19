import os
import orjson
from numpy import array

from typing import (
    Callable,
    List,
    Dict
)


from .philosophy import (
    DBOperation,

    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete,

    Schema,
    Column,
    DBCarrier,

    Log,

    LEVEL,
    DB_TYPE
)

from .joq import JsonQuery
from .utils import getStructher, getKeyList


class FoxBox:
    """
    Foxbox is a operate manager for CRUD and user-self operator definated
    can use in states of memory-cache database and file-based db

    dbom: database operation manager
    """
    level: str = 'set level of operation'

    def operate(self, obj: DBOperation):
        operator: Callable = getattr(self, obj.op_name.lower()+'_op')
        operator(obj)

        if obj.callback:
            if self.level == obj.callback_level:
                obj.callback(obj)


class MemBox(FoxBox):
    level: str = 'memory'

    def create_op(self, obj: DBCreate):
        db = obj.db
        columns = db.columns[1:] # except ID column

        for record in obj.record:
            raw_data = record.dict()
            db.ID.append(db.ID.flag)
            list(map(lambda c: db[c].append(raw_data[c]),columns))


    def read_op(self, obj: DBRead):
        q: JsonQuery = obj.session.query
        q.raw = obj.raw
        obj.record = q.SELECT(*obj.select)\
                      .ORDER_BY(obj.order)\
                      .LIMIT(obj.limit)\
                      .all()
        # TODO in 1.1

    def update_op(self, obj: DBUpdate):
        for record in obj.record:
            raw_data = record.dict()
            ID = record.ID
            list(map(lambda c:obj.db[c].update(ID,raw_data[c]), obj.update))

    def delete_op(self, obj: DBUpdate):
        for ID in obj.record:
            list(map(lambda c:obj.db[c].pop(ID), obj.db.columns))
    #__slots__ = ('_create_op','_level')


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
            cdata = data[_column]
            column = Column(data = cdata)
            db[_column] = column
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
        print(db)
        flag = db.ID.flag
        data = {
            c : list(db[c].data[:flag])
            for c in columns
        }
        print(data) 
        with open(path, mode) as dbfile:
            dbfile.write(orjson.dumps({'db':data}))

    def dump_op(self, obj: DBDump):
        db = obj.db
        self._dump(obj.path, db)

    def create_database_op(self, obj: CreateJsonDB):
        db = obj.structure()
        self._dump(obj.path, db, mode='xb+')  # mode set for check database dosent exists


class LogBox(FoxBox):
    level: str = 'log'

    def operate(self, obj: DBOperation):
        path = '.log'
        log_text = [
            ' ; '.join([*[getattr(log,i) for i in log.__annotations__.keys()], '\n'])
            for log in obj.logs
        ]

        if not os.path.exists(path):
            with open(path, 'w') as log_file:
                log_file.write((' ; '.join([i.upper() for i in Log.__annotations__.keys()])+'\n'))

        with open('.log','a') as log_file:
            log_file.writelines(log_text)


class BoxManager(FoxBox):
    def __init__(self, *box):
        self.boxbox = {bx.level: bx() for bx in box}

    def operate(self, obj):
        levels = set(obj.levels) & self.boxbox.keys()
        for level in levels:
            self.boxbox[level].operate(obj)
