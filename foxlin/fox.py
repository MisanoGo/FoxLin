from typing import List,Dict, Tuple ,Any ,Union
import functools

from pydantic import BaseModel

from philosophy import *
from box import JsonBox,DBLoad, DBDump
from utils import getStructher, getKeyList


class Den(object):
    def __init__(self,
                 db: DBCarrier,
                 schema: Schema,
                 commiter: Callable
            ):
        self.__db: DB_TYPE = db
        self._schema: Schema = schema
        self._commiter = commiter


        self._commit_list: List[CRUDOperation] = []


    @staticmethod
    def commitRecorder(f) -> Callable:
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            r = f(self,*args,*kwargs)
            if isinstance(r,CRUDOperation):
                self._commit_list.append(r)
        return wrapper

    def select(self,ID: int) -> Schema:
        record = {c:self.__db[c][ID] for c in self.columns}
        return self.schema(**record)

    @commitRecorder
    def insert(self, s: Schema) -> DBCreate:
        return DBCreate(record=s)

    @commitRecorder
    def update(self, s: Schema, updated_fields: List[str]) -> DBUpdate:
        return DBUpdate(record=s,updated_fields=updated_fields)

    @commitRecorder
    def delete(self, s: Schema) -> DBDelete:
        return DBUpdate(record=s)

    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())

    def commit(self):
        self._commiter(self._commit_list)
        del self


class FoxLin(FoxBox):
    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
            ):
        self.path =path
        self.schema = schema

        self.rsc_box: FoxBox = JsonBox(self.path, self.schema)
        self.rsc_box.operate(DBLoad(callback=self.load_op))

    def load_op(self, dbc: DBCarrier):
        scl: List[str] = getKeyList(self.schema) # get user definate Schema column list
        dcl: List[str] = dbc.db.keys() # get raw database column

        if scl == dcl:
            self.__db = dbc.db
    
    def _commit(self,commit_list: List[CRUDOperation]):
        list(map(self.operate, commit_list))

        self.rsc_box.operate(DBDump(db=db))

    def session(self) -> Den:
        return Den(self.__db,self.schema,self._commit)

    def read_op(self, obj: DBRead):
        pront(obj)

    def create_op(self, obj: DBCreate):
        print(obj)

    def update_op(self, obj: DBUpdate):
        print(obj)

    def delete_op(self, obj: DBDelete):
        print(obj)
