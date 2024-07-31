from typing import List

from foxlin.core.database import DBCarrier, Schema

from .base import DBOperation, LEVEL, LOG

STORAGE = LEVEL('STORAGE')

class JsonDBOP(DBOperation):
    path: str
    levels: List[LEVEL] = [STORAGE, LOG]
    structure: Schema | None = None

    # TODO : validate path exists with pydantic validator

class CreateJsonDB(JsonDBOP):
    op_name: str = "create_database"

class DBLoad(DBCarrier, JsonDBOP):
    op_name = 'LOAD'

class DBDump(DBCarrier, JsonDBOP):
    op_name = 'DUMP'

