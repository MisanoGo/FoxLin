from typing import List, Dict, Callable, Optional, Generator, Any
from contextlib import contextmanager
import functools
import time


from .query import FoxQuery

from .database import (
    Schema,
    DBCarrier,
    
    DB_TYPE,COLUMN
)

from .operation import (
    CRUDOperation,
    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete
)

from .utils import (
    generate_random_name
)


class Session(object):
    """
    Den is session model for FoxLin DB manager 
    here Den records operations on database and over then commited,
    commit list will send to Foxlin for real operate

    oriented of SQL DML,TCL,DQL logic

    """
    def __init__(self,
                 db: DB_TYPE,
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
        # TODO : also test a way to first get filterd column data by id then export records
        assert ID != None # check for record exists 
        column_list = columns if columns else self._db.columns # set custom or menualy columns

        for _id in ID:
            rec = {c: self._db[c].data[_id] for c in column_list} # rich record as dict
            # check for export data as raw record or initial with Schema
            yield rec if raw else self._schema.construct(**rec)

    @_commitRecorder
    def insert(self, *recs: Schema, columns: List[COLUMN]= None) -> DBCreate:
        if not columns:
            columns = self._db.columns[1:] # except ID
        return DBCreate(record=recs, create=columns, db=self._db)

    @_commitRecorder
    def read(self, **kwargs) -> DBRead:
        # out of service
        return DBRead(**kwargs, session=self)

    @_commitRecorder
    def update(self, *recs: Schema, columns: List[COLUMN]) -> DBUpdate:
        return DBUpdate(record=recs, update=columns, db=self._db)

    @_commitRecorder
    def delete(self, *recs: Schema) -> DBDelete:
        return DBDelete(record=recs, db=self._db)

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


    def discard(self, op: Optional[CRUDOperation] = None) -> None|CRUDOperation:
        # remove specified operation or last operation in commit list
        if op : self._commit_list.remove(op)
        else: return self._commit_list.pop()
        return None

    #__slots__ = ('_insert','_commit','_db','_schema','_commiter','_commit_list')

class SessionManager:
    """Manages sessions with a pool and expiration handling."""

    def __init__(self, db: Any, schema: Any, commiter: Any):
        self._db = db
        self.schema = schema
        self._commiter = commiter
        self._session_pool: Dict[str, Dict[str, Any]] = {}  # Session pool

    def establish_session(self, privileges: set, expire_in: int = 3600) -> Session:
        """
        Create and store a new session with a unique name, privileges, and expiration time.
        """
        session_name = generate_random_name()
        session_instance = {
            'session': Session(self._db, self.schema, self._commiter),
            'privileges': privileges,
            'expires_at': time.time() + expire_in
        }
        self._session_pool[session_name] = session_instance
        
        return session_instance['session']

    def get_session(self, session_name: str) -> Optional[Session]:
        """Retrieve a session by its name."""
        session_info = self._session_pool.get(session_name)
        if session_info and session_info['expires_at'] > time.time():
            return session_info['session']
        else:
            # Remove expired session
            self._session_pool.pop(session_name, None)
            return None

    @property
    def sessionFactory(self) -> Session:
        """Creates and returns a new session instance."""
        return self.establish_session(privileges=set())  # Create a session with default privileges

    @contextmanager
    def session(self, session_name: Optional[str] = None, privileges: set = None):
        """
        Context manager to create and handle a session.
        If session_name is provided, attempt to retrieve that session.
        If not, create a new session with optional privileges.  
        """
        if session_name:
            # Try to retrieve an existing session by name
            session_instance = self.get_session(session_name)
            if session_instance is None:
                raise ValueError(f"Session {session_name} does not exist or has expired.")
        else:
            # Establish a new session with specified privileges or an empty set
            session_instance = self.establish_session(privileges or set())
        try:
            yield session_instance  # Yield the session instance
        finally:
            # Commit changes when exiting context
            session_instance.commit()
            # Optionally remove the session from the pool after use
            self._session_pool.pop(session_name, None)

    __slots__ = ('_session_pool', '_db', 'schema', '_commiter')