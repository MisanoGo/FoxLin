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
def fake_data(table, count=10):
    faker = Faker()
    data = [
        table(
            ID=str(number),
            name=faker.name(),
            family=faker.name(),
            address=faker.address(),
            bio=faker.text(),
            age=random.randint(10, 80)
        ) for number in range(count)
    ]
    return data


class TestFoxLin:
    def dbms(self, table, fake_data):
        path = os.path.join(BASE_DIR, 'tests/db.json')
        if os.path.exists(path):
            os.remove(path)

        foxlin = FoxLin(path, table)

        with foxlin.session as fox_session:
            fox_session.INSERT(*fake_data)
            fox_session.COMMIT()
            foxlin.load()

            query = fox_session.query
            return list(query.SELECT().all())

    def test_dbms_benchmark(self, benchmark, table, fake_data):
        func = self.dbms
        result = benchmark(func, table, fake_data)
        assert result == fake_data
