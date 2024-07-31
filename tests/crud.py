import pytest
from faker import Faker
from foxlin import FoxLin, Schema, column

# Define the schema
class MyTable(Schema):
    name: str = column(dtype=str)
    age: int = column(dtype=int)
    username: str = column(uniqe=True, dtype=str)
    password: str = column(dtype=str)

# Initialize the database
db = FoxLin('./test_db.json', MyTable)  # Use a separate test database

fake = Faker()

@pytest.fixture
def setup_db():
    data = [
        MyTable(name=fake.name(), age=fake.random_int(min=18, max=80), username=fake.unique.user_name(), password=fake.password()),
        MyTable(name=fake.name(), age=fake.random_int(min=18, max=80), username=fake.unique.user_name(), password=fake.password()),
        MyTable(name=fake.name(), age=fake.random_int(min=18, max=80), username=fake.unique.user_name(), password=fake.password()),
        MyTable(name=fake.name(), age=fake.random_int(min=18, max=80), username=fake.unique.user_name(), password=fake.password())
    ]
    with db.session as db_session:
        db_session.insert(*data)
    yield
    # Clean up the database after each test
    with db.session as db_session:
        db_session.delete(list(db.query.all()))

def test_create(setup_db):
    # Verify that records were inserted
    records = db.query.all()
    assert len(records) == 4

def test_read(setup_db):
    # Verify that query works
    query = db.query
    record = query.where(query.age > 17).order_by(query.age).first()
    assert record is not None

def test_update(setup_db):
    # Update a record and verify
    with db.session as db_session:
        record = db.query.where(db.query.username == db.query.first().username).first()
        new_age = fake.random_int(min=18, max=80)
        record.age = new_age
        db_session.update(record)

    updated_record = db.query.where(db.query.username == record.username).first()
    assert updated_record.age == new_age

def test_delete(setup_db):
    # Delete a record and verify
    with db.session as db_session:
        record = db.query.where(db.query.username == db.query.first().username).first()
        db_session.delete(record)

    deleted_record = db.query.where(db.query.username == record.username).first()
    assert deleted_record is None