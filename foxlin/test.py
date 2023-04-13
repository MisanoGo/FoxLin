from random import randint

from faker import Faker 
from mergedeep import merge

from fox import FoxLin, Schema, BASIC_BOX
from box import CreateJsonDB,DBDump,JsonBox

class Person(Schema):
    name: str
    family: str
    address: str
    biography: str
    age: int

ff: Faker = Faker()



data_list = [Person(ID=i,name=ff.name(),family=ff.name(),address=ff.address(),biography=ff.text(),age=randint(17,99)) for i in range(10)]


def gp():
    np = '/'.join(__file__.split('/')[0:-1])
    path = f'{np}/jdbt/{randint(111,99999999999999)}.json'
    print(path)
    cjdb = CreateJsonDB(path=path)
    cjdb.structure = Person
    JsonBox().operate(cjdb)
    return path


def test_my_stuff(benchmark):
    @benchmark
    def fxdb_test():
        f = FoxLin(gp(),Person)
        with f.session as s:
            s.insert(*data_list)
