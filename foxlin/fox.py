from typing import List,Dict, Tuple ,Any ,Union
import functools
from pydantic import BaseModel
from philosophy import *
from box import FoxBox


class FoxLin(object):
    auto_commit: bool = True
    _commit_list: List = []

    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 auto_commit: bool = True,
                 file_system: FileSystem = FoxBox
            ):
        self.path = path
        self.auto_commit = auto_commit
        self._commit_list = []
        self.schema: Schema = schema
        self.file_system = file_system(self.path)

        self.__db: Dict[str,Dict[int,Any]] = {}

        #self.load()

    def load(self):
        self.__db = self.file_system.load().db

    def commit(self,operation:Union[DBOperation,List[DBOperation]] = _commit_list):
        if type(operation) is list:
            for o in operation:
                self.file_system.operate(o)
            self._commit_list.clear()
        else:
            self.file_system.operate(operation)

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
        record = {c:self.__db[c][ID] for c in self.__db.keys()}
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

    def _update_record(self):
        pass

    @_auto_commit
    def update(self) -> DBUpdate:
        # TODO : implement

    def _delete_record(self):
        pass

    @_auto_commit
    def delete(self) -> DBDelete:
        # TODO : implement

    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())
