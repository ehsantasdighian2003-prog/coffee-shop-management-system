from psycopg2.extras import RealDictCursor


class OrderRepository:
    """
    Repository responsible for
    order database operations.
    """

    def __init__(self, conn):
        self.conn = conn

    # =====================================================
    # PRODUCTS
    # =====================================================

    def get_product_by_id(self, product_id: int):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    id,
                    price,
                    stock,
                    is_active
                FROM products
                WHERE id = %s
                """,
                (product_id,),
            )

            return cur.fetchone()

    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(self, user_id: int, total_price):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                INSERT INTO orders
                (
                    user_id,
                    total_price
                )

                VALUES (%s, %s)

                RETURNING id
                """,
                (user_id, total_price),
            )

            return cur.fetchone()

    def create_order_item(self, order_id: int, product_id: int, quantity: int, price):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )

                VALUES (%s, %s, %s, %s)
                """,
                (order_id, product_id, quantity, price),
            )

    # =====================================================
    # STOCK MANAGEMENT
    # =====================================================

    def decrease_stock(self, product_id: int, quantity: int):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                UPDATE products

                SET stock = stock - %s

                WHERE id = %s
                """,
                (quantity, product_id),
            )

    def increase_stock(self, product_id: int, quantity: int):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                UPDATE products

                SET stock = stock + %s

                WHERE id = %s
                """,
                (quantity, product_id),
            )

    # =====================================================
    # UPDATE ORDER
    # =====================================================

    def update_order(self, order_id: int, total_price):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                UPDATE orders

                SET total_price = %s

                WHERE id = %s

                RETURNING
                    id,
                    user_id,
                    total_price,
                    created_at
                """,
                (total_price, order_id),
            )

            return cur.fetchone()

    # =====================================================
    # PAGINATION
    # =====================================================

    def get_orders_paginated(self, limit, offset, search, min_total, max_total, sort):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            query = """
                SELECT
                    id,
                    user_id,
                    total_price,
                    created_at

                FROM orders

                WHERE 1=1
            """

            params = []

            if search:

                query += " AND CAST(user_id AS TEXT) ILIKE %s"

                params.append(f"%{search}%")

            if min_total is not None:

                query += " AND total_price >= %s"

                params.append(min_total)

            if max_total is not None:

                query += " AND total_price <= %s"

                params.append(max_total)

            if sort == "desc":

                query += " ORDER BY created_at DESC"

            else:

                query += " ORDER BY created_at ASC"

            query += """
                LIMIT %s
                OFFSET %s
            """

            params.extend([limit, offset])

            cur.execute(query, params)

            return cur.fetchall()

    def count_orders(self, search=None, min_total=None, max_total=None):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            query = """
                SELECT COUNT(*) AS total

                FROM orders

                WHERE 1=1
            """

            params = []

            if search:

                query += " AND CAST(user_id AS TEXT) ILIKE %s"

                params.append(f"%{search}%")

            if min_total is not None:

                query += " AND total_price >= %s"

                params.append(min_total)

            if max_total is not None:

                query += " AND total_price <= %s"

                params.append(max_total)

            cur.execute(query, params)

            return cur.fetchone()["total"]

    # =====================================================
    # GET ORDERS
    # =====================================================

    def get_order_by_id(self, order_id: int):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    total_price,
                    created_at

                FROM orders

                WHERE id = %s
                """,
                (order_id,),
            )

            return cur.fetchone()

    def get_orders_by_user(self, user_id: int):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    total_price,
                    created_at

                FROM orders

                WHERE user_id = %s

                ORDER BY created_at DESC
                """,
                (user_id,),
            )

            return cur.fetchall()

    def get_order_items(self, order_id: int):

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                SELECT
                    product_id,
                    quantity,
                    price

                FROM order_items

                WHERE order_id = %s

                ORDER BY id
                """,
                (order_id,),
            )

            return cur.fetchall()

    # =====================================================
    # DELETE
    # =====================================================

    def delete_order_items(self, order_id: int):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM order_items

                WHERE order_id = %s
                """,
                (order_id,),
            )

    def delete_order(self, order_id: int):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM orders

                WHERE id = %s
                """,
                (order_id,),
            )
