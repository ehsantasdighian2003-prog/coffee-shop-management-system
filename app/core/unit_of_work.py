from app.core.database import get_connection

from app.repositories.auth_repository import AuthRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.user_repository import UserRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.supplier_repository import SupplierRepository
from app.repositories.purchase_order_repository import PurchaseOrderRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.repositories.product_batch_repository import ProductBatchRepository
from app.repositories.waste_repository import WasteRepository
from app.repositories.inventory_report_repository import InventoryReportRepository
from app.repositories.customer_repository import CustomerRepository


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
        self.inventory: InventoryRepository | None = None
        self.suppliers: SupplierRepository | None = None
        self.purchase_order: PurchaseOrderRepository | None = None
        self.warehouses: WarehouseRepository | None = None
        self.product_batches: ProductBatchRepository | None = None
        self.waste: WasteRepository | None = None
        self.inventory_report: InventoryReportRepository | None = None
        self.customer: CustomerRepository | None = None


    def __enter__(self) -> "UnitOfWork":

        self.conn = get_connection()

        self.products = ProductRepository(self.conn)

        self.orders = OrderRepository(self.conn)

        self.categories = CategoryRepository(self.conn)

        self.users = UserRepository(self.conn)

        self.auth = AuthRepository(self.conn)

        self.reports = ReportRepository(self.conn)
        
        self.inventory = InventoryRepository(self.conn)

        self.suppliers = SupplierRepository(self.conn)

        self.purchase_order = PurchaseOrderRepository(self.conn)

        self.warehouses = WarehouseRepository(self.conn)

        self.product_batches = ProductBatchRepository(self.conn)

        self.waste = WasteRepository(self.conn)

        self.inventory_report = InventoryReportRepository(self.conn)

        self.customer = CustomerRepository(self.conn)

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
                
                
    def commit(self):
        self.conn.commit()
        
        
    def rollback(self):
        self.conn.rollback()