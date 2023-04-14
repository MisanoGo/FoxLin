import pytest
import random
import os

from faker import Faker

from foxlin.fox import FoxLin, Schema

from config.settings import BASE_DIR


@pytest.fixture(scope="session")
def table():
    class Person(Schema):
        name: str
        family: str
        address: str
        bio: str
        age: int
    return Person


@pytest.fixture(scope="session")
def fake_data(table):
    faker = Faker()
    data = [
        table(
            ID=number,
            name=faker.name(),
            family=faker.name(),
            address=faker.address(),
            bio=faker.text(),
            age=random.randint(10, 80)
        ) for number in range(10)
    ]
    return data


class TestFoxLin:
    def dbms(self, table, fake_data):
        path = os.path.join(BASE_DIR, 'tests/test.json')
        if os.path.exists(path):
            os.remove(path)

        foxlin = FoxLin(path, table)

        with foxlin.session as fox_session:
            fox_session.INSERT(*fake_data)
            fox_session.COMMIT()
            foxlin.load()
            return list(fox_session.SELECT().get())

    def test_dbms_benchmark(self, benchmark, table, fake_data):
        func = self.dbms
        result = benchmark(func, table, fake_data)
        assert result == fake_data
