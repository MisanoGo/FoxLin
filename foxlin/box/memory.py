from typing import List

from .fox import FoxBox

from foxlin.query import FoxQuery
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
    create : List[COLUMN]

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
        columns = obj.create # except ID column

        def insert(record):
            flag = db.ID.plus()
            tuple(map(lambda col: db[col].__setitem__(flag, record[col]), columns))

        tuple(map(insert, obj.record))


    def read_op(self, obj: DBRead):
        # out of service
        q: FoxQuery = obj.session.query
        q.raw = obj.raw
        obj.record = q.SELECT(*obj.select)\
                      .ORDER_BY(obj.order)\
                      .LIMIT(obj.limit)\
                      .all()
        # TODO in 1.1

    def update_op(self, obj: DBUpdate):
        columns = obj.update
        for record in obj.record:
            _id = obj.db.ID.getv(record.ID)
            list(map(lambda col: obj.db[col].update(_id, record[col]), columns))

    def delete_op(self, obj: DBDelete):
        for _id in obj.record:
            _id = obj.db.ID.getv(_id)
            list(map(lambda c:obj.db[c].pop(_id), obj.db.columns))

    __slots__ = ('_create_op','_update_op','_delete_op','_level')

