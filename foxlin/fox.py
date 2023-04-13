import os
from typing import List

from .philosophy import Schema, CRUDOperation
from .den import DenManager
from .box import (
    BoxManager,
    FoxBox,
    MemBox,
    JsonBox,
    LogBox,
    CreateJsonDB,

    DBLoad,
    DBDump,
)

BASIC_BOX = [MemBox, JsonBox, LogBox]


class FoxLin(BoxManager, DenManager):
    """

    """
    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 box: List[FoxBox] = BASIC_BOX
                 ):

        self.path = path
        self.schema = schema

        super(FoxLin, self).__init__(*box)

    def load(self):
        dbdo = DBLoad(
                callback=self.__set_db,
                callback_level=JsonBox.level,
                path=self.path)

        dbdo.structure = self.schema
        self.operate(dbdo)

    def create_database(self):
        file_path = self.path
        if os.path.exists(file_path):
            raise Exception

        json_db = CreateJsonDB(path=file_path)
        json_db.structure = self.schema
        JsonBox().operate(json_db)


    def __set_db(self, obj: DBLoad):
        self._db = obj.db

    def _commiter(self, commit_list: List[CRUDOperation]):  # call when session.commit() called
        list(map(self.operate, commit_list))
        self.operate(DBDump(db=self._db, path=self.path))
