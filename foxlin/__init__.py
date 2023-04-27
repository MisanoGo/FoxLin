"""

Foxlin is a simple, fast, funny json dbms base on python

usage: simple usage :
from foxlin import FoxLin, Schema


class MyTable(schema): # define your teble schema
    name: str
    username: str
    password: str

db = FoxLin('./db.json', MyTable)

data = [
    MyTable(name='sobhan', username='misano', password='#197382645#'),
    MyTable(name='Tommy', username='god_of_war', password='123QWEasdZXC')
]

with db.session as db_session:
    db_session.INSERT(*data)

# OR 

db_session = db.sessionFactory
db_session.INSERT(*data)
db_session.COMMIT()

r_data = db_session.SELECT().WHERE('name','=','sobhan').get()
myrecord = r_data[0]

print(myrecord.name, myrecord.username, myrecord.password)

"""



from foxlin.fox import FoxLin, BASIC_BOX
from foxlin.sophy import Schema, Column

__all__ = ('FoxLin', 'BASIC_BOX', 'Schema','Column')
