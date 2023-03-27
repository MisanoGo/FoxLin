from typing import List,Dict, Tuple ,Any ,Union
from pydantic import BaseModel
from philosophy import *
from box import FoxBox

class FoxLin(object):
    auto_commit: bool = True
    _commit_list: List = []

    def __init__(self, path: str,
                 schema: Schema,
                 auto_commit: bool=True,
                 file_system: FileSystem = FoxBox
            ):
        self.path = path
        self.auto_commit = auto_commit  
        self.schema: Schema = schema
        self.file_system = file_system(self.path)

        self.__db: Dict[str,Dict[int,Any]] = {}

        self.load()

    def load(self):
        self.__db = self.file_system.load()

    def commit(self,operation:Union[DBOperation,List[DBOperation]] = _commit_list):
        if type(operation) is list:
            for o in operation:
                self.file_system.operate(o)
        else:
            self.file_system.operate(o)

    def _auto_commit(self,f,*args,**kwargs):
        com = f(*args,**kwargs)

        if self.auto_commit :
            self.commit(com)
        else :
            self._commit_list.append(com)
    
    def select(self,ID: int) -> Dict[str,Any]:
        record = {c:self.__db[c][ID] for c in self.__db.keys()}
        return self.schema(**record)

    def query(self):
        pass

    def insert(self,s: Schema):
        for c in self.columns:
            self._insert_record(ID,c,data[c])
        return DBCreate(s)

    def _insert_record(self,ID:int, column: str, data: Any):
        self.__db[column][ID] = data
    
    def _delete_record(self):
        pass

    def delete(self):
        for c in self.columns:
            pass


    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())
