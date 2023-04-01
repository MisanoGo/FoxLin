from typing import List,Dict, Tuple ,Any ,Union
import functools

from pydantic import BaseModel

from philosophy import *
from box import FoxBox,JsonBox, MemBox, LogBox,DBLoad
from den import DenManager

from utils import getStructher, getKeyList


BASIC_BOX = MemBox(JsonBox(LogBox()))


class FoxLin(DenManager):
    """

    """
    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 box: FoxBox = BASIC_BOX,

                 ):
        self.path = path
        self.box = box
        self._schema = schema
        self._commiter = self._commit

        dbdo = DBLoad(
                callback = self.load_op,
                callback_level = JsonBox.level,
                path=path)

        self.box.operate(dbdo)

    def load_op(self, dbc: DBCarrier):
        print(dbc)
        scl: List[str] = getKeyList(self._schema) # get user definate Schema column list
        dcl: List[str] = dbc.db.keys() # get raw database column

        if scl == dcl: # validate database columns with schema columns
            self.__db = dbc.db
    
    def _commit(self,commit_list: List[CRUDOperation]):
        list(map(self.box.perate, commit_list))

        self.parent.operate(DBDump(db=self.__db))


