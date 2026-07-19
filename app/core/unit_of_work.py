from app.core.database import get_connection

from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository


class UnitOfWork:
    """
    Manages database connection and repositories.

    Usage:

        with UnitOfWork() as uow:
            user = uow.users.get_user_by_id(
                uow.conn,
                1
            )

    """

    def __init__(self):

        self.conn = None

        self.products = None
        self.orders = None
        self.categories = None
        self.users = None


    def __enter__(self):

        self.conn = get_connection()

        self.products = ProductRepository()
        self.orders = OrderRepository()
        self.categories = CategoryRepository()
        self.users = UserRepository()

        return self


    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        if self.conn:

            try:

                if exc_type is None:
                    self.conn.commit()

                else:
                    self.conn.rollback()

            finally:

                self.conn.close()