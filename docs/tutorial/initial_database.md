# FoxLin DBMS

after define your table schema
now must initail your db

```Python
from foxlin import FoxLin

db = FoxLin(path, schema)
```

for managing you can disable auto_setup
in auto setup FoxLin go to try create database
& at the end load database

```
db = FoxLin(..., auto_setup=False)
# so if your path not exists create it with :

db.create_database()

# any way at the finally you must load your db
db.load()
```

FoxLin combined from Box Manager & Den manager(den is alias for session)
Box in foxlin is the level of operating of operations
just now we have 3 box:
* JsonBox : handle operations at file level : level = 'jsonfile'
* MemBox  : handle operations at memory level : leve = 'memory'
* LogBox  : handle log's of operations created in process : level = 'log'

in every time of program life
you can disable or enable box's

for example you just need in memory db
and dont need to save it in file
so initail database like this:
```Python
db = FoxLin(schema=MyTable, auto_setup=False, auto_enable=False)
# now all box are disable, let's enable memory box

db.enable_box('memory')
```


