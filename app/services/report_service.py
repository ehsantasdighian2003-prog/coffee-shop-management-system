from decimal import Decimal

from app.core.database import get_connection
from app.repositories.report_repository import ReportRepository
from app.schemas.report import (
    DashboardReport,
    SalesReport,
)


class ReportService:
    """
    Service layer for reports.
    """


    @staticmethod
    def normalize_decimal(
        value
    ) -> Decimal:
        """
        Convert database Decimal values
        into clean API output.
        """

        return Decimal(value).quantize(
            Decimal("1")
        )


    # ==================================================
    # SALES REPORT
    # ==================================================

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


    # ==================================================
    # DASHBOARD REPORT
    # ==================================================

    def get_dashboard_report(self) -> DashboardReport:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_dashboard_statistics()


            return DashboardReport(

                users=data["users"],

                products=data["products"],

                categories=data["categories"],

                orders=data["orders"],


                total_revenue=self.normalize_decimal(
                    data["total_revenue"]
                ),


                average_order_value=self.normalize_decimal(
                    data["average_order_value"]
                ),

            )

        finally:
            conn.close()