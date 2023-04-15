# **_FoxLin_**
simple, fast, funny json dbms base on python

### Quick access :
 - docs : [todo]()
 - pypi : [todo]()
 - code : [todo]()


### Futures :
>   - TODO


## simple usage : 
```Python
    from foxlin import FoxLin, Schema

    class MyTable(schema): # define your teble schema
        name: str
        age: int
        username: str
        password: str

    db = FoxLin('./db.json', MyTable)

    data = [
        MyTable(name='brian', age=37, username='biran1999', password='123456789')
        MyTable(name='sobhan', age=20, username='misano', password='#197382645#'),
        MyTable(name='Tommy', age=15, ageusername='god_of_war', password='123QWEasdZXC')
    ]

    with db.session as db_session:
        db_session.INSERT(*data)

    # OR 

    db_session = db.sessionFactory
    db_session.INSERT(*data)
    db_session.COMMIT()

    query = db_session.SELECT()
    record = query.WHERE(query.age > 17).first()
    

    print(record.name, record.username, record.password)
```

##### TODO in 1.0
- [x] crud
- [x] level base operation manager
- [x] self log system
- [x] session model
- [x] transaction but by grouping commits **not ACDI**
- [ ] write test
- [x] neo dict implemented by numpy
- [ ] add logs to .<database-name>.logs
- [ ] genetate logs
- [x] quering

##### TODO at 1.1
- asynchronus
- transaction ACDI

