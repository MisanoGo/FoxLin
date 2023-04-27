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

##### undo action's
in FoxLin you can undo your action's
```Python
si = session.insert(...) # methods return operation data class
su = session.update(...)
sd = session.delete(...)

session.discard() # return sd
session.discard(si) # remove si operation

s.commit() # su will apply
```

##### SAVE POINT, ROLLBACK: change commit line
TODO 
``` Python
si = session.insert(...)
su = session.update(...)
sd = session.delete(...)

# transfer operation to 'sv_name' and clear main op list
session.savepoint('sv_name')
session.commit() # no change

# return operation in 'sv_name' in main op list
session.rollback('sv_name')
session.rollback() # will clear main op list

session.add_op(si) # add operation to op list
session.savepoint('sv_name')

session.commit('sv_name') # commit operation in 'sv_name'

session._commit_list # main op list
session._commit_point # saved points
```
