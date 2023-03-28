from typing import List,Dict, Tuple ,Any ,Union
import functools

from pydantic import BaseModel

from philosophy import *
from box import JsonBox,DBLoad


class FoxLin(object):
    auto_commit: bool = True
    _commit_list: List[CRUDOperation] = []

    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 auto_commit: bool = True,
                 file_system: FoxBox = JsonBox
            ):
        self.path = path
        self.auto_commit = auto_commit
        self._commit_list = []
        self.schema: Schema = schema
        self.file_system = file_system(self.path)

        self.__db: DB_TYPE = {}

        self.commit(DBLoad(callback=OperatorCarrier(func=self._validate)))

    def _load(self, dbc: DBCarrier):
        self.__db = dbc.db

    def _validate(self, dbc: DBCarrier) -> bool:
        scl: List[str] = self.schema.construct().schema()['properties'].keys() # get user definate Schema column list
        dcl: List[str] = dbc.db.keys() # get raw database column

        if scl == dcl:
            self._load(dbc)

    def commit(self,*operation: Tuple[CRUDOperation]):
        for o in operation:
            self.file_system.operate(o)

    @staticmethod
    def _auto_commit(f):
        @functools.wraps(f)
        def op(self,*args,**kwargs):
            com = f(self,*args,**kwargs)
            if self.auto_commit :
                self.commit(com)
            else :
                self._commit_list.append(com)
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
        return DBCreate(record=s)

    def _update_record(self,ID: int, column: str, data: Any):
        self.__db[column][ID] = data

    @_auto_commit
    def update(self,s: Schema, updated_fields:List[str]) -> DBUpdate:
        for c in updated_fields:
            self._update_record(s.ID,c,s.dict()[c])
        return DBUpdate(record=s)

    def _delete_record(self, ID: int, column: str):
        self.__db[column].pop(ID)

    @_auto_commit
    def delete(self, s: Schema) -> DBDelete:
        for c in self.columns:
            self._delete_record(s.ID,c)
        return DBDelete(record=s)

    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())
