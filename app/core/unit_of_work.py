from typing import Optional, Type

from app.core.database import get_connection

from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository


class UnitOfWork:
    """
    Manages database connection,
    transaction lifecycle,
    and repository instances.
    """

    def __init__(self):

        self.conn = None

        self.products: Optional[ProductRepository] = None
        self.orders: Optional[OrderRepository] = None
        self.categories: Optional[CategoryRepository] = None
        self.users: Optional[UserRepository] = None
        self.auth: Optional[AuthRepository] = None


    def __enter__(self) -> "UnitOfWork":

        self.conn = get_connection()

        self.products = ProductRepository(
            self.conn
        )

        self.orders = OrderRepository(
            self.conn
        )

        self.categories = CategoryRepository(
            self.conn
        )

        self.users = UserRepository(
            self.conn
        )

        self.auth = AuthRepository(
            self.conn
        )

        return self


    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback,
    ) -> None:

        if self.conn:

            try:

                if exc_type is None:
                    self.conn.commit()

                else:
                    self.conn.rollback()

            finally:

                self.conn.close()