from pydantic import BaseModel

class Schema(BaseModel):
    ID: int


class DatabaseOperation(BaseModel):
    op_name: str
    structure: Schema

class DBCreate(DatabaseOperation):
    pass

class DBRead(DatabaseOperation):
    pass

class DBUpdate(DatabaseOperation):
    pass

class DBDelete(DatabaseOperation):
    pass
