from cProfile import run
import pytest
import random
import os

from faker import Faker

from foxlin import FoxLin, Schema, Column

from config.settings import BASE_DIR


@pytest.fixture(scope="session")
def table():
    class Person(Schema):
        name: str = Column()
        family: str = Column()
        address: str = Column()
        bio: str = Column()
        age: int = Column()
    return Person


@pytest.fixture(scope="session")
def fake_data(table, count=1000):
    faker = Faker()
    data = [
        table(
            name=faker.name(),
            family=faker.name(),
            address=faker.address(),
            bio=faker.text(),
            age=random.randint(10, 80)
        ) for _ in range(count)
    ]
    return data

@pytest.fixture(scope="session")
def db(table):
    path = os.path.join(BASE_DIR, 'tests/db.json')
    if os.path.exists(path):
        os.remove(path)

    foxlin = FoxLin(path, table)
    return foxlin

@pytest.fixture(scope="session")
def session(db):
    return db.sessionFactory

class TestFoxLin:
    def test_insert(self, fake_data, session):
        session.insert(*fake_data)
        session.commit()

        #q = session.query
        #assert list(q.all()) == fake_data

    def itest_read(self, session):
        q = session.query
        q.raw = True
        rec = q.select('name','age','ID') \
               .order_by('age')\
               .limit(5)\
               .all()

        def _(obj):
            assert list(rec) == list(obj.record)

        session.read(
            callback = _,
            callback_level = 'memory',
            raw = True,
            select= ['name','age','ID'],
            limit = 5,
            order = 'age'
        )
        session.commit()

    def test_update(self, session):
        q = session.query
        p1 = q.rand()
        p2 = p1.copy()
        p2.age = 19
        session.update(p2, columns=['age'])
        session.commit()
        
        query = session.query
        assert query.get_one(p1.ID) != p1
        assert query.get_by_id(p1.ID).age == p2.age

    def test_delete(self, session):
        q = session.query
        rand_rec = q.rand()

        session.delete(rand_rec.ID)
        session.commit()

        q = session.query
        q.raw = True
        assert rand_rec.dict() not in tuple(q.all())

    def test_io_speed(self, benchmark, fake_data, session):
        func = self.test_insert
        benchmark(func, fake_data, session)

    def test_memory_speed(self, benchmark, fake_data, db):
        db.disable_box('storage') # remove filedb manager box : DUMP, LOAD will not work
        func = self.test_insert
        benchmark(func, fake_data, db.sessionFactory)

    def test_read_speed(self, benchmark, session):
        f = lambda : list(session.query.all())
        benchmark(f)


