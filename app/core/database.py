from contextlib import contextmanager

import psycopg2

from app.core.config import settings


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():

    return psycopg2.connect(
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
    )


# =========================
# CONNECTION MANAGER
# =========================

@contextmanager
def get_db():

    conn = get_connection()

    try:

        yield conn

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()