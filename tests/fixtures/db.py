import pytest

from app.core.database import get_connection


@pytest.fixture
def db_connection():

    conn = get_connection()

    try:
        yield conn

    finally:
        conn.rollback()
        conn.close()
