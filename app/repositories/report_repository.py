from typing import Any

from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


class ReportRepository:
    """
    Repository responsible for application reports.
    """


    def __init__(
        self,
        conn: connection
    ):
        self.conn = conn


    # ==================================================
    # DASHBOARD STATISTICS
    # ==================================================

    def get_dashboard_statistics(self) -> dict[str, Any]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    (
                        SELECT COUNT(*)
                        FROM users
                        WHERE deleted_at IS NULL
                    ) AS users,


                    (
                        SELECT COUNT(*)
                        FROM products
                    ) AS products,


                    (
                        SELECT COUNT(*)
                        FROM categories
                    ) AS categories,


                    (
                        SELECT COUNT(*)
                        FROM orders
                    ) AS orders,


                    (
                        SELECT COALESCE(
                            SUM(total_price),
                            0
                        )
                        FROM orders
                    ) AS total_revenue,


                    (
                        SELECT COALESCE(
                            AVG(total_price),
                            0
                        )
                        FROM orders
                    ) AS average_order_value

                """
            )

            return cur.fetchone()


    # ==================================================
    # SALES REPORT
    # ==================================================

    def get_sales_report(self) -> dict[str, Any]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    COUNT(id) AS total_orders,


                    COALESCE(
                        SUM(total_price),
                        0
                    ) AS total_revenue,


                    COALESCE(
                        AVG(total_price),
                        0
                    ) AS average_order_value


                FROM orders
                """
            )

            return cur.fetchone()