from typing import List, Dict, Callable, Optional, Generator
from contextlib import contextmanager
import functools

from .query import FoxQuery

from .sophy import (
    Schema,
    DBCarrier,
    DB_TYPE,

)

from .box import (
    CRUDOperation,
    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete
)


class Den(object):
    """
    Den is session model for FoxLin DB manager here
    Den records operations on database and over then commited,
    commit list will send to Foxlin for real operate

    oriented of SQL DML,TCL,DQL logic

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
        # record exported operation & append them to commit list
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            robj = f(self, *args, **kwargs)
            if isinstance(robj, CRUDOperation):
                self._add_op(robj)
            return robj
        return wrapper

    def _add_op(self, obj):
        self._commit_list.append(obj)

    @property
    def query(self):
        return FoxQuery(self)

    def get_one(self, ID: int, columns=None, raw: bool=False) -> Schema | Dict:
        r = list(self.get_many(ID, columns=columns, raw=raw))[0]
        return r

    def get_many(self, *ID: int, columns=None, raw: bool = False) -> Generator:
        assert ID != None # check for record exists 
        column_list = columns if columns else self._db.columns # set custom or menualy columns

        for _id in ID:
            rec = {c: self._db[c][_id] for c in column_list} # rich record as dict
            # check for export data as raw record or initial with Schema
            yield rec if raw else self._schema.construct(**rec)

    @_commitRecorder
    def insert(self, *s: Schema) -> DBCreate:
        return DBCreate(record=s, db=self._db)

    @_commitRecorder
    def read(self, **kwargs) -> DBRead:
        return DBRead(**kwargs, session=self)

    @_commitRecorder
    def update(self, *s: Schema, updated_fields: List[str]) -> DBUpdate:
        return DBUpdate(record=s, update=updated_fields, db=self._db)

    @_commitRecorder
    def delete(self, *ID: int) -> DBDelete:
        return DBDelete(record=ID, db=self._db)

    def commit(self, savepoint: Optional[str] = None):
        if savepoint:
            self._commiter(self._commit_point[savepoint])
            self._commit_point.pop(savepoint)
        else :
            self._commiter(self._commit_list)
        self.rollback()

    def rollback(self, savepoint: Optional[str] = None):
        self._commit_list = self._commit_point[savepoint] if savepoint else []
        if savepoint : self._commit_point.pop(savepoint)

    def savepoint(self, name: str):
        self._commit_point[name] = self._commit_list
        self.rollback()


    def discard(self, op: Optional[CRUDOperation] = None):
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
        s.commit()
        del s

    __slots__ = ('_session', '_sessionFactory')
