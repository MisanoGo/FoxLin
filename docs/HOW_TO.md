# HOW TO

# TODO : write discription

### how to : disable log
```Python
db = FoxLin(...)
db.disable_box('log')
```

### how to : use just in memory
```Python
db = FoxLin(..., auto_setup=False)
db.disable_box('jsonfile') # return True if success
```


