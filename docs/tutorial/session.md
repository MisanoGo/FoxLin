# Session

for every operation on data of db you need session
Den just is alias name for session it means home of Fox
```
db = FoxLin(...)

session = db.sessionFactory

OR

with db.session as session:
    # some operation
    ...
```

session also look like curser in SQL lib's
so operation not work in real time 
their going to stay at list of operation's
and need to commit to go in operating procces

in context manager after exit commit method will called by context manager
so it is auto commit state

but in session must call commit handly

```
session = db.sessionFactory
session.delete(17)
session.commit()

# in context manager

with db.session as session:
    session.delete(17)
# auto call commit()
```
