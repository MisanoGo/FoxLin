from typing import List

from .fox import FoxBox

from foxlin.query import JsonQuery
from foxlin.sophy import (
    Schema,
    DBOperation, 
    DBCarrier,

    ID,
    COLUMN,
    LEVEL,
)



class CRUDOperation(DBOperation, DBCarrier):
    levels: List[LEVEL] = ['memory', 'log']
    record: Schema | List[Schema]


class DBCreate(CRUDOperation):
    op_name: str = 'CREATE'

class DBRead(CRUDOperation):
    op_name: str = "READ"
    session: object
    raw: bool = False

    select: List[COLUMN] | None = None
    limit: int | None = None
    where: List[tuple] | None = None
    order: str | None = None
    record: List[Schema] | None = None
    # TODO in 1.1 group & having

class DBUpdate(CRUDOperation):
    op_name: str = "UPDATE"
    update: List[COLUMN]

class DBDelete(CRUDOperation):
    op_name: str = "DELETE"

    record: List[ID]



class MemBox(FoxBox):
    level: str = 'memory'

    def create_op(self, obj: DBCreate):
        db = obj.db
        columns = db.columns[1:] # except ID column

        for record in obj.record:
            raw_data = record.dict()
            flag = db.ID.plus()
            list(map(lambda c: db[c].__setitem__(flag,raw_data[c]),columns))


    def read_op(self, obj: DBRead):
        q: JsonQuery = obj.session.query
        q.raw = obj.raw
        obj.record = q.SELECT(*obj.select)\
                      .ORDER_BY(obj.order)\
                      .LIMIT(obj.limit)\
                      .all()
        # TODO in 1.1

    def update_op(self, obj: DBUpdate):
        for record in obj.record:
            raw_data = record.dict()
            _id = obj.db.ID.getv(record.ID)
            list(map(lambda c:obj.db[c].update(_id,raw_data[c]), obj.update))

    def delete_op(self, obj: DBUpdate):
        for _id in obj.record:
            list(map(lambda c:obj.db[c].pop(_id), obj.db.columns[1:]))

    #__slots__ = ('_create_op','_level')

