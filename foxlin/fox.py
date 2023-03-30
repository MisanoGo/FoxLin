from typing import List,Dict, Tuple ,Any ,Union
import functools

from pydantic import BaseModel

from philosophy import *
from box import JsonBox,DBLoad, DBDump


class FoxLin(object):
    auto_commit: bool = True
    _commit_rate: int = 0

    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 auto_commit: bool = True,
                 commit_rate: int = 10,
                 file_system: FoxBox = JsonBox
            ):
        self.path = path
        self.auto_commit = auto_commit
        self.commit_rate = commit_rate
        self.schema: Schema = schema
        self.file_system = file_system(self.path, self.schema)

        self.__db: DB_TYPE = {}

        self.commit(DBLoad(callback=self._validate))

    def _load(self, dbc: DBCarrier):
        self.__db = dbc.db
        print(type(dbc.db['ID']))

    def _validate(self, dbc: DBCarrier):
        scl: List[str] = self.schema.construct().schema()['properties'].keys() # get user definate Schema column list
        dcl: List[str] = dbc.db.keys() # get raw database column

        if scl == dcl:
            self._load(dbc)

    def commit(self,operation: DBDump):
        return self.file_system.operate(operation)

    @staticmethod
    def _auto_commit(f):
        @functools.wraps(f)
        def op(self,*args,**kwargs):
            self._commit_rate += 1
            com = f(self,*args,**kwargs)

            if self._commit_rate >= self.commit_rate:
                self.commit(DBDump(db=self.__db))
                self._commit_rate = 0
        return op

    def select(self,ID: int) -> Schema:
        record = {c:self.__db[c][ID] for c in self.columns}
        return self.schema(**record)

    def query(self):
        pass

    def _insert_record(self,ID:int, column: str, data: Any):
        self.__db[column][ID] = data

    @_auto_commit
    def insert(self,s: Schema) -> DBCreate:
        row_data = s.dict()
        for c in self.columns:
            self._insert_record(s.ID,c,row_data[c])

    def _update_record(self,ID: int, column: str, data: Any):
        self.__db[column][ID] = data

    @_auto_commit
    def update(self,s: Schema, updated_fields:List[str]) -> DBUpdate:
        for c in updated_fields:
            self._update_record(s.ID,c,s.dict()[c])

    def _delete_record(self, ID: int, column: str):
        self.__db[column].pop(ID)

    @_auto_commit
    def delete(self, s: Schema) -> DBDelete:
        for c in self.columns:
            self._delete_record(s.ID,c)

    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())
