from psycopg2.extras import RealDictCursor


class InventoryRepository:
    """
    Repository responsible for inventory transaction operations.
    """

    def __init__(self, conn):
        self.conn = conn

    # =====================================================
    # GET PRODUCT
    # =====================================================

    def get_product_by_id(self, product_id):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    stock,
                    is_active
                FROM products
                WHERE id = %s
                """,
                (product_id,),
            )

            return cursor.fetchone()

    # =====================================================
    # UPDATE STOCK
    # =====================================================

    def update_product_stock(self, product_id, stock):

        with self.conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE products
                SET stock = %s
                WHERE id = %s
                """,
                (
                    stock,
                    product_id,
                ),
            )

    # =====================================================
    # CREATE INVENTORY TRANSACTION
    # =====================================================

    def create_transaction(
        self,
        product_id,
        transaction_type,
        quantity,
        note=None,
        created_by=None,
        supplier_id=None,
        order_id=None,
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                INSERT INTO inventory_transactions
                (
                    product_id,
                    change_type,
                    quantity,
                    reason,
                    created_by,
                    supplier_id,
                    order_id
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING *
                """,
                (
                    product_id,
                    transaction_type,
                    quantity,
                    note,
                    created_by,
                    supplier_id,
                    order_id,
                ),
            )

            result = cursor.fetchone()

                # Map database fields to API response fields
        if result:
            result["transaction_type"] = result.pop("change_type")
            result["note"] = result.pop("reason")

        return result
    
    
    def get_product_history(self, product_id: int):
        query = """
            SELECT
                id,
                product_id,
                change_type,
                quantity,
                reason,
                created_at
            FROM inventory_transactions
            WHERE product_id = %s
            ORDER BY created_at DESC
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (product_id,))
            rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "product_id": row["product_id"],
                "transaction_type": row["change_type"],
                "quantity": float(row["quantity"]),
                "note": row["reason"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]
        
        
    def get_stock_movements(self):

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

        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            {
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "total_in": int(row["total_in"]),
                "total_out": int(row["total_out"]),
                "current_stock": int(row["current_stock"]),
            }
            for row in rows
        ]
        
        
    def get_transaction_by_id(
        self,
        transaction_id: int,
    ):
        query = """
            SELECT
                id,
                product_id,
                change_type,
                quantity,
                reason,
                supplier_id,
                order_id,
                created_at
            FROM inventory_transactions
            WHERE id = %s
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute(
                query,
                (transaction_id,),
            )

            return cursor.fetchone()
        