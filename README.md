
![# **_FoxLin_** ](./poster.png)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)


### philosophy
Foxlin is developed to create the best User experience of DBMS interface for mini projects
it is fast because use of numpy array for contain columns data in memory
and using pydantic for manage data in program

also have powerfull process managers.

### feature
 * simple & fast
 * friendly ux
 * auto backup
 * nosql structure
 * power full query tool based on sql concept
 * logging
 * async #TODO in 1.1
 * smart cache system # TODO in 1.2
 * query cache system # TODO in 1.2

### Quick access :
 - [docs](https://GitHub.com/MirS0bhan/FoxLin/blob/stable/docs)
 - [pypi](https://pypi.org/project/foxlin/)
 - [code](https://GitHub.com/MirS0bhan/FoxLin)


### requirements
 * numpy
 * pydantic
 * orjson

## installation

### from pypi
```console
$ pip install foxlin
```

### from github
``` console
$ git clone https://github.com/MisanoGo/FoxLin && cd FoxLin
$ pytest # run tests
$ poetry install
$ poetry build 
$ pip install dist/foxlin-*.whl
```

## simple usage :
```Python
from foxlin import FoxLin, Schema, column

class MyTable(Schema):
    # define your teble schema
    name: str = column(dtype=str)
    age: int = column(dtype=int)
    username: str = column(uniqe=True, dtype=str)
    password: str = column(dtype=str)

db = FoxLin('./db.json', MyTable) # create db

data = [
    MyTable(name='brian', age=37, username='biran1999', password='123456789'),
    MyTable(name='sobhan', age=20, username='misano', password='#197382645#'),
    MyTable(name='Tommy', age=15, username='god_of_war', password='123QWEasdZXC'),
    MyTable(name='Ali', age=20, username='p_1969_q', password='@QWE123KFH@')
]

with db.session as db_session:
    db_session.insert(*data)
    # auto commit in the end of context manager

query = db.query
record = query.where(query.age > 17, query.name == 'Ali').order_by(query.age).first()

print(record.name, record.username, record.password)
```

### Note
 - every crud operation on db has O(record_count * column_count) order


**my experience from this project**
 * in operations with high order, when have many static if,else(no change in all of program)
 it's better to split their by classes and use factory clasess for select own usefull class, etc : columns.py:column


## TODO

##### TODO at 1.0.0
− implement memory & storage box with rust/zig
- asynchronus
- transaction ACDI
- define Group By & HAVING
- log time duration of operation's 
- migrate
- stub
- data compretion
- memory cache system
- query cache system
- session privilege's
- multi table
- ...


