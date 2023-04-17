from typing import List, Dict, Callable, Optional
from contextlib import contextmanager
import functools

from .joq import JsonQuery
from .philosophy import (
    Schema,
    DBCarrier,
    DB_TYPE,
    DBOperation,
    CRUDOperation,

    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete,
)


class Den(object):
    """
    Den is session model for FoxLin DB manager here
    Den records operations on database and over then commited,
    commit list will send to Foxlin for real operate

   oriented by SQL DML,TCL,DQL logic

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
        self._commit_point: Dict[str,List] = {}

    @staticmethod
    def _commitRecorder(f) -> Callable:
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            r = f(self, *args, **kwargs)
            if isinstance(r, CRUDOperation):
                self._commit_list.append(r)
            return r
        return wrapper

    @property
    def query(self):
        return JsonQuery(self)

    def get_by_id(self, ID: str, columns=None, raw: bool = False) -> Schema:
        column_list = columns if columns else self._db.keys()
        record = {c:self._db[c][ID] for c in column_list}
        record = record if raw else self._schema.construct(**record) if columns else self._schema(**record)
        return record

    @_commitRecorder
    def INSERT(self, *s: Schema) -> DBCreate:
        return DBCreate(record=s, db=self._db)

    @_commitRecorder
    def UPDATE(self, *s: Schema, updated_fields: List[str]) -> DBUpdate:
        return DBUpdate(record=s, updated_fields=updated_fields, db=self._db)

    @_commitRecorder
    def DELETE(self, *ID: int) -> DBDelete:
        return DBDelete(record=ID, db=self._db)

    def COMMIT(self, savepoint: Optional[str] = None):
        if savepoint:
            self._commiter(self._commit_point[savepoint])
            self._commit_point.pop(savepoint)
        else :
            self._commiter(self._commit_list)
        self.ROLLBACK()

    def ROLLBACK(self, savepoint: Optional[str] = None):
        self._commit_list = self._commit_point[savepoint] if savepoint else []
        if savepoint : self._commit_point.pop(savepoint)

    def SAVEPOINT(self, name: str):
        self._commit_point[name] = self._commit_list
        self.ROLLBACK()


    def discard(self, op: Optional[DBOperation] = None):
        # remove specified operation or last operation in commit list
        if op : self._commit_list.remove(op)
        else: self._commit_list.pop()

    #__slots__ = ('_insert','_commit','_db','_schema','_commiter','_commit_list')


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
        s.COMMIT()
        del s

    __slots__ = ('_session', '_sessionFactory')
