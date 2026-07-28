from decimal import Decimal

from app.core.database import get_connection
from app.repositories.report_repository import ReportRepository
from app.schemas.report import SalesReport


class ReportService:
    """
    Service layer for reports.
    """

    @staticmethod
    def normalize_decimal(value) -> Decimal:
        """
        Convert database Decimal values
        into clean API numbers.
        """

        return Decimal(value).quantize(
            Decimal("1")
        )


    def get_sales_report(self) -> SalesReport:

        conn = get_connection()

        try:
            repository = ReportRepository(conn)

            data = repository.get_sales_report()

            return SalesReport(
                total_orders=data["total_orders"],
                total_revenue=self.normalize_decimal(
                    data["total_revenue"]
                ),
                average_order_value=self.normalize_decimal(
                    data["average_order_value"]
                ),
            )

        finally:
            conn.close()