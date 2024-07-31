import pytest
import random
import os

from faker import Faker

from foxlin import FoxLin, Schema, column

import os

from pathlib import Path

BASE_DIR = os.path.realpath(Path(__file__).parent.parent)


@pytest.fixture(scope="session")
def table():
    class Person(Schema):
        name: str = column(dtype=str)
        family: str = column(dtype=str)
        address: str = column(dtype=str)
        bio: str = column(dtype=str)
        age: int = column(dtype=int)
    return Person


@pytest.fixture(scope="session")
def fake_data(table, count=100):
    faker = Faker()
    data = [
        table(
            name=faker.name(),
            family=faker.name(),
            address=faker.address(),
            bio=faker.color(),
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

    def test_raw_read_speed(self, benchmark, db):
        query = db.query
        query.raw = True
        f = lambda query : list(query.all())
        benchmark(f, query)
