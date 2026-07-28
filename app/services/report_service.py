from decimal import Decimal

from app.core.database import get_connection
from app.repositories.report_repository import ReportRepository
from app.schemas.report import (
    CustomerReport,
    DashboardReport,
    MonthlySalesReport,
    SalesReport,
    TopProductReport,
    MonthlySalesReport,
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


    # ==================================================
    # TOP PRODUCTS REPORT
    # ==================================================

    def get_top_products(
        self,
        limit: int = 5
    ) -> list[TopProductReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_top_products(
                limit
            )


            return [

                TopProductReport(

                    product_name=item["product_name"],

                    total_sold=item["total_sold"],

                    revenue=self.normalize_decimal(
                        item["revenue"]
                    ),

                )

                for item in data

            ]

        finally:
            conn.close()
            
            
    # ==================================================
    # MONTHLY SALES REPORT
    # ==================================================

    def get_monthly_sales_report(
        self
    ) -> list[MonthlySalesReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_monthly_sales_report()


            return [
                MonthlySalesReport(
                    month=item["month"],

                    total_orders=item["total_orders"],

                    revenue=self.normalize_decimal(
                        item["revenue"]
                    ),
                )

                for item in data
            ]

        finally:
            conn.close()
            
            
    # ==================================================
    # CUSTOMER ANALYTICS REPORT
    # ==================================================

    def get_customer_report(
        self,
    ) -> list[CustomerReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_customer_analytics()

            return [
                CustomerReport(
                    customer_id=item["customer_id"],
                    username=item["username"],
                    total_orders=item["total_orders"],
                    total_spent=self.normalize_decimal(
                        item["total_spent"]
                    ),
                    average_order_value=self.normalize_decimal(
                        item["average_order_value"]
                    ),
                )
                for item in data
            ]

        finally:
            conn.close()