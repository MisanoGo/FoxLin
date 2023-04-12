import pytest
import random
import os

from faker import Faker

from foxlin.fox import FoxLin, Schema, BASIC_BOX
from foxlin.box import CreateJsonDB, DBDump, JsonBox

from main import BASE_DIR


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


@pytest.fixture(scope="session")
def generate_file(table):
    file_path = os.path.join(BASE_DIR, "tests/test.json")
    if os.path.exists(file_path):
        os.remove(file_path)
    json_db = CreateJsonDB(path=file_path)
    json_db.structure = table
    JsonBox().operate(json_db)
    return file_path


class TestFoxLin:
    def test_dbms(self, table, fake_data, generate_file):
        foxlin = FoxLin(generate_file, table)
        with foxlin.session as fox_session:
            fox_session.insert(*fake_data)
            fox_session.commit()
            foxlin.load()
            assert fox_session.SELECT().get() == fake_data
