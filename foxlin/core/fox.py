import os
from typing import List

from .sophy import Schema 
from .den import DenManager
from .box import (
    FoxBox,
    MemBox,
    LogBox,

    StorageBox,
    CreateJsonDB,
    DBLoad,
    DBDump,

    BoxManager,
    CRUDOperation
)

from foxlin.errors import (
    DataBaseExistsError,
    InvalidDatabaseSchema
)


BASIC_BOX = [MemBox(), StorageBox(), LogBox()]

class FoxLin(BoxManager, DenManager):
    """
    simple, fast, funny python column based dbms

    Parameters
    ----------
    path: str = None
        database path

    schema: Schema = Schema
        define table columns structure

    box: List[FoxBox] = BASIC_BOX
        determine operations endpoint operate stage

    auto_setup: bool = True
        auto create and load database, db will created if db not exists

    auto_enable: bool = True
        for manage box activity
    """
    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 box: List[FoxBox] = BASIC_BOX,
                 auto_setup: bool = True,
                 auto_enable: bool = True
                 ):

        self.path = path
        self.schema = schema
        self._db = self.schema()

        super(FoxLin, self).__init__(*box, auto_enable=auto_enable)
        if auto_setup : self.auto_setup()

    def auto_setup(self):
        try:
            self.create_database()
        except DataBaseExistsError:
            pass
        finally:
            # TODO set Exception for invalid Schema state
            self.load()

    def load(self):
        dbdo = DBLoad(
                callback=self.__set_db,
                callback_level= StorageBox.level,
                path=self.path)

        dbdo.structure = self.schema
        self.operate(dbdo)

    def __set_db(self, op: DBLoad):
        self._db = op.db

    def create_database(self):
        file_path = self.path
        if os.path.exists(file_path): raise DataBaseExistsError(file_path)

        cjdbo = CreateJsonDB(path=file_path) # cjdbo: create json database operation
        cjdbo.structure = self.schema
        self.operate(cjdbo)


    def _commiter(self, commit_list: List[CRUDOperation]):
        """
        work when session.commit() called
        to send operation to the box manager
        """
        list(map(self.operate, commit_list))
        self.operate(DBDump(db=self._db, path=self.path))
        # aplly change of database from memory to file-based db


