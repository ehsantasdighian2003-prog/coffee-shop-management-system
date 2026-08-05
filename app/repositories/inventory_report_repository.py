from psycopg2.extras import RealDictCursor


class InventoryReportRepository:
    """
    Repository for inventory reports.
    """

    def __init__(
        self,
        conn,
    ):
        self.conn = conn
        
        
    # =====================================================
    # STOCK SUMMARY REPORT
    # =====================================================

    def get_stock_summary(self):

        query = """
            SELECT
                id AS product_id,
                name AS product_name,
                stock AS current_stock
            FROM products
            ORDER BY name;
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(query)

            return cursor.fetchall()
        
        
    # =====================================================
    # INVENTORY MOVEMENT REPORT
    # =====================================================

    def get_inventory_movements(self):

        query = """
            SELECT
                p.id AS product_id,
                p.name AS product_name,

                COALESCE(
                    SUM(
                        CASE
                            WHEN it.change_type = 'IN'
                            THEN it.quantity
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_in,

                COALESCE(
                    SUM(
                        CASE
                            WHEN it.change_type = 'OUT'
                            THEN it.quantity
                            ELSE 0
                        END
                    ),
                    0
                ) AS total_out,

                p.stock AS current_stock

            FROM products p

            LEFT JOIN inventory_transactions it
                ON p.id = it.product_id

            GROUP BY
                p.id,
                p.name,
                p.stock

            ORDER BY p.name;
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(query)

            return cursor.fetchall()
        
        
    # =====================================================
    # WASTE COST REPORT
    # =====================================================

    def get_waste_cost_report(self):

        query = """
            SELECT
                p.id AS product_id,
                p.name AS product_name,

                COALESCE(
                    SUM(w.quantity),
                    0
                ) AS total_quantity,

                COALESCE(
                    SUM(w.cost),
                    0
                ) AS total_cost

            FROM products p

            LEFT JOIN waste_records w
                ON p.id = w.product_id

            GROUP BY
                p.id,
                p.name

            HAVING
                COUNT(w.id) > 0

            ORDER BY
                p.name;
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(query)

            return cursor.fetchall()
        
        
    # =====================================================
    # WAREHOUSE STOCK REPORT
    # =====================================================

    def get_warehouse_stock_report(self):

        query = """
            SELECT
                w.id AS warehouse_id,
                w.name AS warehouse_name,

                p.id AS product_id,
                p.name AS product_name,

                wi.quantity

            FROM warehouse_inventory wi

            JOIN warehouses w
                ON w.id = wi.warehouse_id

            JOIN products p
                ON p.id = wi.product_id

            ORDER BY
                w.name,
                p.name;
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(query)

            return cursor.fetchall()
        
        
    # =====================================================
    # EXPIRING BATCH REPORT
    # =====================================================

    def get_expiring_batches(
        self,
        days: int = 30,
    ):

        query = """
            SELECT
                pb.id AS batch_id,

                pb.product_id,

                p.name AS product_name,

                pb.warehouse_id,

                w.name AS warehouse_name,

                pb.batch_number,

                pb.quantity,

                pb.expiration_date

            FROM product_batches pb

            JOIN products p
                ON p.id = pb.product_id

            JOIN warehouses w
                ON w.id = pb.warehouse_id

            WHERE pb.expiration_date <= (
                CURRENT_DATE + (%s * INTERVAL '1 day')
            )

            ORDER BY
                pb.expiration_date;
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (days,),
            )

            return cursor.fetchall()