from app.core.database import get_connection

from app.repositories.auth_repository import AuthRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.user_repository import UserRepository


class UnitOfWork:
    """
    Manages database connection,
    transaction lifecycle,
    and repository instances.
    """

    def __init__(self):

        self.conn = None

        self.products: ProductRepository | None = None
        self.orders: OrderRepository | None = None
        self.categories: CategoryRepository | None = None
        self.users: UserRepository | None = None
        self.auth: AuthRepository | None = None
        self.reports: ReportRepository | None = None


    def __enter__(self) -> "UnitOfWork":

        self.conn = get_connection()

        self.products = ProductRepository(self.conn)

        self.orders = OrderRepository(self.conn)

        self.categories = CategoryRepository(self.conn)

        self.users = UserRepository(self.conn)

        self.auth = AuthRepository(self.conn)

        self.reports = ReportRepository(self.conn)

        return self


    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
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