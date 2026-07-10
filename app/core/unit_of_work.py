from app.core.database import get_connection


class UnitOfWork:
    """
    Manages a single database transaction.

    Usage:
        with UnitOfWork() as uow:
            repository.some_method(uow.conn)
    """

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = get_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            try:
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            finally:
                self.conn.close()