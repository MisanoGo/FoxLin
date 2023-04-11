from typing import List, Callable
from contextlib import contextmanager
import functools


from philosophy import (
    Schema,
    DBCarrier,
    DB_TYPE,
    CRUDOperation,

    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete,
)

class Den(object):
    """
    Den is session model for FoxLin DB manager
    here Den records operations on database and over then commited, commit list will send to Foxlin for real operate
    """
    def __init__(self,
                 db: DBCarrier,
                 schema: Schema,
                 commiter: Callable
            ):
        self._db: DB_TYPE = db
        self._schema: Schema = schema
        self._commiter = commiter


        self._commit_list: List[CRUDOperation] = []


    @staticmethod
    def _commitRecorder(f) -> Callable:
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            r = f(self,*args,**kwargs)
            if isinstance(r,CRUDOperation):
                self._commit_list.append(r)
        return wrapper

    def select(self,ID: int) -> Schema:
        record = {c:self._db[c][ID] for c in self.columns}
        return self.schema(**record)

    @_commitRecorder
    def insert(self, *s: Schema) -> DBCreate:
        return DBCreate(record = s,
                        db = self._db
                        )

    @_commitRecorder
    def update(self, s: Schema, updated_fields: List[str]) -> DBUpdate:
        return DBUpdate(record=s,updated_fields=updated_fields)

    @_commitRecorder
    def delete(self, s: Schema) -> DBDelete:
        return DBDelete(record=s)

    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())

    def commit(self):
        self._commiter(self._commit_list)
        self._commit_list = []

    __slots__ = ('_insert','_commit','_db','_schema','_commiter','_commit_list')

class DenManager(object):

    @property
    def sessionFactory(self):
        s = Den(
                self._db,
                self.schema,
                self._commiter)
        return s

    @property
    @contextmanager
    def session(self):
        s = self.sessionFactory
        yield s
        s.commit()
        del s

    __slots__ = ('_session','_sessionFactory')
