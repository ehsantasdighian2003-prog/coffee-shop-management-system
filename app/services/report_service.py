from decimal import Decimal

from app.core.database import get_connection
from app.repositories.report_repository import ReportRepository
from app.schemas.report import (
    CategoryPerformanceReport,
    CustomerReport,
    DailySalesReport,
    DashboardReport,
    LowStockReport,
    MonthlySalesReport,
    SalesReport,
    TopProductReport,
    WeeklySalesReport,
    RevenueTrendReport,
    YearlySalesReport,
    YearlyMonthlySales,
    BestSellingHour,
    ProfitProductReport,
    ProfitReport,
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
            
            
    # ==================================================
    # LOW STOCK REPORT
    # ==================================================

    def get_low_stock_products(
        self,
        threshold: int = 10,
    ) -> list[LowStockReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_low_stock_products(threshold)

            return [
                LowStockReport(
                    id=item["id"],
                    name=item["name"],
                    stock=item["stock"],
                )
                for item in data
            ]

        finally:
            conn.close()
            
            
    # ==================================================
    # CATEGORY PERFORMANCE REPORT
    # ==================================================

    def get_category_performance(
        self,
    ) -> list[CategoryPerformanceReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_category_performance()

            return [
                CategoryPerformanceReport(
                    category_name=item["category_name"],
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
    # DAILY SALES REPORT
    # ==================================================

    def get_daily_sales_report(
        self,
    ) -> list[DailySalesReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_daily_sales_report()


            return [
                DailySalesReport(
                    date=item["date"],
                    total_orders=item["total_orders"],
                    revenue=self.normalize_decimal(
                        item["revenue"]
                    ),
                    average_order_value=self.normalize_decimal(
                        item["average_order_value"]
                    ),
                )

                for item in data
            ]

        finally:
            conn.close()
            
            
    # ==================================================
    # WEEKLY SALES REPORT
    # ==================================================

    def get_weekly_sales_report(
        self
    ) -> list[WeeklySalesReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_weekly_sales_report()


            return [

                WeeklySalesReport(
                    week=item["week"],

                    total_orders=item["total_orders"],

                    revenue=self.normalize_decimal(
                        item["revenue"]
                    ),

                    average_order_value=self.normalize_decimal(
                        item["average_order_value"]
                    ),
                )

                for item in data

            ]

        finally:
            conn.close()
            
            
    # ==================================================
    # REVENUE TREND REPORT
    # ==================================================

    def get_revenue_trend(
        self,
    ) -> list[RevenueTrendReport]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_revenue_trend()


            return [

                RevenueTrendReport(

                    date=item["date"],

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
    # YEARLY SALES REPORT
    # ==================================================

    def get_yearly_sales_report(
        self,
        year: int
    ) -> YearlySalesReport:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_yearly_sales_report(
                year
            )


            total_orders = sum(
                item["total_orders"]
                for item in data
            )


            total_revenue = sum(
                (
                    item["revenue"]
                    for item in data
                ),
                Decimal("0")
            )


            return YearlySalesReport(

                year=year,

                total_orders=total_orders,

                total_revenue=self.normalize_decimal(
                    total_revenue
                ),

                monthly_sales=[

                    YearlyMonthlySales(

                        month=int(
                            item["month"]
                        ),

                        total_orders=item["total_orders"],

                        revenue=self.normalize_decimal(
                            item["revenue"]
                        ),

                    )

                    for item in data

                ],
            )


        finally:

            conn.close()
            
            
    # ==================================================
    # BEST SELLING HOURS REPORT
    # ==================================================

    def get_best_selling_hours(
        self,
    ) -> list[BestSellingHour]:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            data = repository.get_best_selling_hours()

            return [

                BestSellingHour(
                    hour=item["hour"],
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
    # PROFIT REPORT
    # ==================================================

    def get_profit_report(
        self,
    ) -> ProfitReport:

        conn = get_connection()

        try:

            repository = ReportRepository(conn)

            summary = repository.get_profit_summary()

            products = repository.get_profit_report()

            return ProfitReport(

                total_revenue=self.normalize_decimal(
                    summary["total_revenue"]
                ),

                total_cost=self.normalize_decimal(
                    summary["total_cost"]
                ),

                total_profit=self.normalize_decimal(
                    summary["total_profit"]
                ),

                products=[

                    ProfitProductReport(

                        product_name=item["product_name"],

                        total_sold=item["total_sold"],

                        revenue=self.normalize_decimal(
                            item["revenue"]
                        ),

                        cost=self.normalize_decimal(
                            item["cost"]
                        ),

                        profit=self.normalize_decimal(
                            item["profit"]
                        ),

                        )

                    for item in products

                ],

            )

        finally:

            conn.close()
            
