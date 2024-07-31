from typing import List, Optional, Union

from foxlin.core.database import (
    DBCarrier,
    Schema,
    
    ID,
    LEVEL,
    COLUMN
)

from .base import DBOperation, LOG

# Define memory level constant
MEMORY = LEVEL('MEMORY')

class CRUDOperation(DBOperation, DBCarrier):
    """Base class for CRUD operations."""
    levels: List[LEVEL] = [MEMORY, LOG]
    record: Union[Schema, List[Schema]]

class DBCreate(CRUDOperation):
    """Class for creating records in the database."""
    op_name: str = 'CREATE'
    create: List[COLUMN]

class DBRead(CRUDOperation):
    """Class for reading records from the database."""
    op_name: str = "READ"
    session: object
    raw: bool = False
    
    select: Optional[List[COLUMN]] = None
    limit: Optional[int] = None
    where: Optional[List[tuple]] = None
    order: Optional[str] = None
    record: Optional[List[Schema]] = None
    # TODO: Implement group & having in version 1.1

class DBUpdate(CRUDOperation):
    """Class for updating records in the database."""
    op_name: str = "UPDATE"
    update: List[COLUMN]

class DBDelete(CRUDOperation):
    """Class for deleting records from the database."""
    op_name: str = "DELETE"