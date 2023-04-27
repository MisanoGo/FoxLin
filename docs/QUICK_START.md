# QUICK START

### define table schema
```Python
from foxlin import Schema, Column, UniqeColumn

class MyTable(Schema):
    name    : str = Column()
    age     : int = Column()
    username: str = UniqeColumn()
```

### initial db instance
```Python
from foxlin import FoxLin

db_path = './db.json' # set path of database

db = FoxLin(db_path, MyTable)
```

## CRUD

### insert
```Python
data = MyTable(
            name = 'tom',
            age  = 17,
            username = 'tomtom')

# insert data
with db.session as session:
    session.insert(data)
```

### update
```
# update data
data.age = 18
session.update(data, updated_field=['age'])
```

### delete
``` Python
# delete data
session.delete(data.ID)
```

## Query
### get query
``` Python
query = session.query
# OR
query = db.query
```

### select columns
```
query.select('age','name')
```

### get records
```Python
# get first record
record = query.first()

# get end
record = query.end()

# get random record
record = query.rand()

# get all
records = query.select('age','username').all() # return generator
record_list = list(records)
```

### access column data
```Python
name_data = query.name
age_data = query.age
```

### filter records
```Python
filterd_rec = query.select('username').where(q.age > 50, q.name == 'some name').first()
```

### sort records
```
sorted_recs = query.where(query.age == 17).select('age').order_by(query.age).first()
```

### max, min, mean
``` Python
query.where(query.age == 17)
query.order_by(query.age)

max_rec = query.max()
min_rec = query.min()
mean_rec = query.mean()
```

### limit records
```
10_rec = query.limit(10).all()
```
