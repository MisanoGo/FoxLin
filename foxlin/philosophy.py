from abc import ABC, abstractstaticmethod

from pydantic import BaseModel

class Schema(BaseModel):
    ID: int


class DBOperation(BaseModel):
    op_name: str
    record : Schema

class DBCreate(DBOperation):
    pass

class DBRead(DBOperation):
    pass

class DBUpdate(DBOperation):
    pass

class DBDelete(DBOperation):
    pass

class FileSystem(ABC):
    @abstractstaticmethod
    def load(self):
        pass

    @abstractstaticmethod
    def operate(self, obj: DBOperation):
        pass
