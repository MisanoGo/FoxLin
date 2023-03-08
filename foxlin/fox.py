from typing import List,Dict, Tuple ,Any ,Union
import functools

from pydantic import BaseModel

from philosophy import *
from box import FoxBox, JsonBox, MemBox, LogBox, DBLoad, DBDump, BoxManager
from den import DenManager

from utils import getStructher, getKeyList


BASIC_BOX = [MemBox,JsonBox,LogBox]


class FoxLin(BoxManager,DenManager):
    """

    """
    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 box: FoxBox = BASIC_BOX
                 ):
        self.path = path
        self._schema = schema
        self._commiter = self._commit

        super(FoxLin, self).__init__(*box)

        dbdo = DBLoad(
                callback = self.__set_db,
                callback_level = JsonBox.level,
                levels = [JsonBox.level,LogBox.level],
                path = path)

        dbdo.structure = schema
        self.operate(dbdo)

    def __set_db(self, obj: DBLoad):
        self._db = obj.db
    
    def _commit(self,commit_list: List[CRUDOperation]):
        list(map(self.operate,commit_list))
        self.operate(DBDump(db=self._db,path=self.path))


