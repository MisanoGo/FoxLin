FoxLin use pydantic for alias db table structure
alse use it for contain column data

how schema will define:
class MyTable(Schema):
    \<field name\>:\<type\> = \<column type\>

#### Column types:
 * Column
 * UniqeColumn
 * RaiColumn

##### first step:
```Python
from foxlin import Schema, Column, UniqeColumn, RaiColumn

class MyTable(Schema):
    # ID: int|str = IDColumn()
    # ID column are implemented in Schema, don't need to define it
    name: str = Column()
    age : int = Column()

    username : str = UniqeColumn() # uniqe columns also are RaiColumn
```

##### create records
```Python
record = MyTable(name='sobhan', age=17, username='misano')
```

