# **_FoxLin_**
simple, fast, funny column base dbms on python

### philosophy
Foxlin developed to create best User experience of DBMS interface for mini projects
it is fast because use of numpy array for contain columns data in memory
and using pydantic for manage data in program

also have powerfull process managers.

### Quick access :
 - docs : [todo]()
 - pypi : [todo]()
 - code : [todo]()


#### requirements
 - numpy
 - pydantic
 - orjson

# installation
```console
$ pip install foxlin
```

## simple usage :
```Python
from foxlin import FoxLin, Schema, Column, UniqeColumn

class MyTable(schema): 
    # define your teble schema
    # set your own column type needed, splited for low order and high performance
    name: str = Column()
    age: int = Column
    username: str = UniqeColumn()
    password: str = Column()

db = FoxLin('./db.json', MyTable) # create db

data = [
    MyTable(name='brian', age=37, username='biran1999', password='123456789')
    MyTable(name='sobhan', age=20, username='misano', password='#197382645#'),
    MyTable(name='Tommy', age=15, username='god_of_war', password='123QWEasdZXC')
    MyTable(name='Ali', age=20, username='p_1969_q', password='@QWE123KFH@')
]

with db.session as db_session:
    db_session.insert(*data)
    # auto commit after end of context manager

# OR 

db_session = db.sessionFactory
db_session.insert(*data)
db_session.commit()

query = db_session.query
record = query.where(query.age > 17, query.name == Ali).order_by('age').first()

print(record.name, record.username, record.password)
```

## TODO

##### TODO in 1.0
- [x] crud
- [x] level base operation manager
- [x] self log system
- [x] session model
- [x] transaction but by grouping commits **not ACDI**
- [x] write test
- [x] benchmarck test
- [x] add logs to .logs file
- [x] define logs in operation statment and able to setting by user
- [ ] generate logs
- [x] quering

##### TODO at 1.1
- asynchronus
- transaction ACDI
- define Group By & HAVING
- log operation's time duration
- migrate

##### TODO at 1.2
- memory cache system
- query cache system
- session privilege's
- multi table
- ...

