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


    # ==================================================
    # TOP PRODUCTS REPORT
    # ==================================================

    def get_top_products(
        self,
        limit: int = 5
    ) -> list[dict[str, Any]]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    p.name AS product_name,


                    SUM(oi.quantity) AS total_sold,


                    SUM(
                        oi.quantity * oi.price
                    ) AS revenue


                FROM order_items oi


                INNER JOIN products p
                    ON p.id = oi.product_id


                INNER JOIN orders o
                    ON o.id = oi.order_id


                GROUP BY p.name


                ORDER BY total_sold DESC


                LIMIT %s;

                """,
                (limit,)
            )

            return cur.fetchall()
        
        
    # ==================================================
    # MONTHLY SALES REPORT
    # ==================================================

    def get_monthly_sales_report(
        self
    ) -> list[dict[str, Any]]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    TO_CHAR(
                        created_at,
                        'YYYY-MM'
                    ) AS month,


                    COUNT(id) AS total_orders,


                    COALESCE(
                        SUM(total_price),
                        0
                    ) AS revenue


                FROM orders


                GROUP BY
                    TO_CHAR(
                        created_at,
                        'YYYY-MM'
                    )


                ORDER BY month ASC;

                """
            )

            return cur.fetchall()
        
        
    # ==================================================
    # CUSTOMER ANALYTICS REPORT
    # ==================================================

    def get_customer_analytics(self):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    u.id AS customer_id,

                    u.username,


                    COUNT(o.id) AS total_orders,


                    COALESCE(
                        SUM(o.total_price),
                        0
                    ) AS total_spent,


                    COALESCE(
                        AVG(o.total_price),
                        0
                    ) AS average_order_value


                FROM users u


                LEFT JOIN orders o

                    ON o.user_id = u.id


                WHERE u.deleted_at IS NULL


                GROUP BY
                    u.id,
                    u.username


                HAVING COUNT(o.id) > 0


                ORDER BY total_spent DESC

                """
            )

            return cur.fetchall()