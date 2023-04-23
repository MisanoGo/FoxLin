# **_FoxLin_**
simple, fast, funny column base dbms on python

### philosophy
TODO

### Quick access :
 - docs : [todo]()
 - pypi : [todo]()
 - code : [todo]()


### Futures :
>   - TODO


## simple usage : 
```Python
from foxlin import FoxLin, Schema, Column, UniqeColumn

class MyTable(schema): # define your teble schema
    name: str = Column()
    age: int = Column
    username: str = Column()
    password: str = Column()

db = FoxLin('./db.json', MyTable) # create db / auto_setup will create database and load

data = [
    MyTable(name='brian', age=37, username='biran1999', password='123456789')
    MyTable(name='sobhan', age=20, username='misano', password='#197382645#'),
    MyTable(name='Tommy', age=15, username='god_of_war', password='123QWEasdZXC')
    MyTable(name='Ali', age=20, username='p_1969_q', password='@QWE123KFH@')
]

with db.session as db_session:
    db_session.INSERT(*data)
    # auto commit after end of context manager

# OR 

db_session = db.sessionFactory
db_session.INSERT(*data)
db_session.COMMIT()

query = db_session.query
record = query.WHERE(query.age > 17, query.name == Ali).ORDER_BY('age').first()

print(record.name, record.username, record.password)
```

##### TODO in 1.0
- [x] crud
- [x] level base operation manager
- [x] self log system
- [x] session model
- [x] transaction but by grouping commits **not ACDI**
- [x] write test
- [ ] benchmarck test
- [x] add logs to .logs file
- [ ] define logs in operation statment and able to setting by user
- [ ] generate logs
- [x] quering

##### TODO at 1.1
- asynchronus
- transaction ACDI
- define Group By & HAVING
- log operation's time duration
- migrate

##### TODO at 1.2
- cache system
- session privilege's
- ...

