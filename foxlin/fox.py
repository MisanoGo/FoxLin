from typing import List,Dict, Tuple ,Any ,Union
import functools

from pydantic import BaseModel

from philosophy import *
from box import JsonBox,DBLoad, DBDump
from den import DenManager

from utils import getStructher, getKeyList


class FoxLin(FoxBox,DenManager):
    """

    """
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

        if scl == dcl: # validate database columns with schema columns
            self.__db = dbc.db
    
    def _commit(self,commit_list: List[CRUDOperation]):
        list(map(self.operate, commit_list))

        self.rsc_box.operate(DBDump(db=self.__db))

    def read_op(self, obj: DBRead):
        pront(obj)

    def create_op(self, obj: DBCreate):
        print(obj)

    def update_op(self, obj: DBUpdate):
        print(obj)

    def delete_op(self, obj: DBDelete):
        print(obj)
