import pytest
from db.database import AttendanceDB

# set PYTHONPATH=.

@pytest.fixture(scope="module")
def db():
    return AttendanceDB("test_db")

def test_add_member(db):
    db.add_member("Alice", "Shen Yue")
    assert db.is_member("Alice", "Shen Yue")
