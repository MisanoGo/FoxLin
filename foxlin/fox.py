from typing import List,Dict, Tuple ,Any ,Union
from pydantic import BaseModel
from mirfire.philosophy import *


class FoxLin(object):
    auto_commit: bool = True
    _commit_list: List = []

    def __init__(self, path: str,
                 schema: Schema,
                 auto_commit: bool=True
            ):
        self.path = path
        self.auto_commit = auto_commit  
        self.schema: Schema = schema

        self.__db: Dict[str,Dict[int,Any]] = {}

        self.load()

    def load(self):
        self.__db = self._load_from_csvp()
 
    def _load_from_csvp(self):
        rdb: str = open(self.path,'r').read()
        rw : List[str] = rdb.splitlines()
        cl: List[str] = rw[0].split(';') # column list
        dl: List[str] = rw[1:] # data List

        db = {c:{} for c in cl} #load columns into db
        for d in dl:
            rd = d.split(';')
            ID = int(rd[0]) # specifed Id of row data
            for c,i in zip(cl,rd):
                db[c][ID] = i
        return db

    def _export_to_csvp(self):
        pass

    def commit(self,operation:Union[DatabaseOperation,List[DatabaseOperation]] = _commit_list):
        pass

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
