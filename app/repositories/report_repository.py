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
        
        
    # ==================================================
    # LOW STOCK REPORT
    # ==================================================

    def get_low_stock_products(
        self,
        threshold: int = 10,
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    id,

                    name,

                    stock

                FROM products

                WHERE

                    stock <= %s

                    AND is_active = TRUE

                ORDER BY

                    stock ASC,
                    name ASC
                """,
                (threshold,),
            )

            return cur.fetchall()
        
        
    # ==================================================
    # CATEGORY PERFORMANCE REPORT
    # ==================================================

    def get_category_performance(self):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    c.name AS category_name,

                    COALESCE(
                        SUM(oi.quantity),
                        0
                    ) AS total_sold,

                    COALESCE(
                        SUM(
                            oi.quantity * oi.price
                        ),
                        0
                    ) AS revenue

                FROM categories c

                LEFT JOIN products p
                    ON p.category_id = c.id

                LEFT JOIN order_items oi
                    ON oi.product_id = p.id

                GROUP BY
                    c.id,
                    c.name

                HAVING
                    COALESCE(SUM(oi.quantity), 0) > 0

                ORDER BY
                    revenue DESC,
                    category_name ASC
                """
            )

            return cur.fetchall()
        
        
    # ==================================================
    # DAILY SALES REPORT
    # ==================================================

    def get_daily_sales_report(self):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    DATE(created_at) AS date,

                    COUNT(id) AS total_orders,

                    COALESCE(
                        SUM(total_price),
                        0
                    ) AS revenue,

                    COALESCE(
                        AVG(total_price),
                        0
                    ) AS average_order_value


                FROM orders


                GROUP BY
                    DATE(created_at)


                ORDER BY
                    date DESC
                """
            )

            return cur.fetchall()
        
        
    # ==================================================
    # WEEKLY SALES REPORT
    # ==================================================

    def get_weekly_sales_report(self) -> list[dict[str, Any]]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    TO_CHAR(
                        DATE_TRUNC(
                            'week',
                            created_at
                        ),
                        'IYYY-"W"IW'
                    ) AS week,


                    COUNT(id) AS total_orders,


                    COALESCE(
                        SUM(total_price),
                        0
                    ) AS revenue,


                    COALESCE(
                        AVG(total_price),
                        0
                    ) AS average_order_value


                FROM orders


                GROUP BY
                    DATE_TRUNC(
                        'week',
                        created_at
                    )


                ORDER BY
                    DATE_TRUNC(
                        'week',
                        created_at
                    ) DESC

                """
            )

            return cur.fetchall()
        
        
    # ==================================================
    # REVENUE TREND REPORT
    # ==================================================

    def get_revenue_trend(self) -> list[dict[str, Any]]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    DATE(created_at) AS date,


                    COUNT(id) AS total_orders,


                    COALESCE(
                        SUM(total_price),
                        0
                    ) AS revenue


                FROM orders


                GROUP BY
                    DATE(created_at)


                ORDER BY
                    date ASC

                """
            )

            return cur.fetchall()
        
        
    # ==================================================
    # YEARLY SALES REPORT
    # ==================================================

    def get_yearly_sales_report(
        self,
        year: int
    ) -> list[dict[str, Any]]:

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                SELECT

                    EXTRACT(
                        MONTH FROM created_at
                    ) AS month,


                    COUNT(id) AS total_orders,


                    COALESCE(
                        SUM(total_price),
                        0
                    ) AS revenue


                FROM orders


                WHERE EXTRACT(
                    YEAR FROM created_at
                ) = %s


                GROUP BY
                    EXTRACT(
                        MONTH FROM created_at
                    )


                ORDER BY
                    month ASC;

                """,
                (year,)
            )

            return cur.fetchall()