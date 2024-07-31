from foxlin.core.columns.concrete import ConcreteColumn

c = ConcreteColumn()

c.insert(10)
print(c.sorted_data,'\n',c.data)
c.insert(20)
print(c.sorted_data,'\n',c.data)
c.insert(50)
print(c.sorted_data,'\n',c.data)
c.insert(40)
print(c.sorted_data,'\n',c.data)
c.insert(100)
print(c.sorted_data,'\n',c.data)
print(c.get(3))