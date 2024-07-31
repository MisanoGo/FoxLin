from foxlin import FoxLin, Schema, column

class MyTable(Schema):
    # define your teble schema
    name: str = column(dtype=str)
    age: int = column(dtype=int)
    username: str = column(dtype=str)
    password: str = column(dtype=str)

db = FoxLin('./basic.json', MyTable) # create db

data = [
    MyTable(name='brian', age=37, username='biran1999', password='123456789'),
]

with db.session as db_session:
    db_session.insert(*data)
    # auto commit in the end of context manager

query = db.query
record = query.where(query.age > 17, query.name == 'Ali').order_by(query.age).first()

print(record.name, record.username, record.password)