from psycopg2.extras import RealDictCursor


class OrderRepository:

    # =====================================================
    # PRODUCTS
    # =====================================================

    @staticmethod
    def get_product_by_id(conn, product_id: int):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
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

    @staticmethod
    def create_order(conn, user_id: int, total_price: float):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO orders (user_id, total_price)
                VALUES (%s, %s)
                RETURNING id
                """,
                (user_id, total_price),
            )
            return cur.fetchone()

    @staticmethod
    def create_order_item(
        conn,
        order_id: int,
        product_id: int,
        quantity: int,
        price: float,
    ):
        with conn.cursor() as cur:
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
                (
                    order_id,
                    product_id,
                    quantity,
                    price,
                ),
            )

    # =====================================================
    # STOCK
    # =====================================================

    @staticmethod
    def decrease_stock(conn, product_id: int, quantity: int):
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE products
                SET stock = stock - %s
                WHERE id = %s
                """,
                (quantity, product_id),
            )

    @staticmethod
    def increase_stock(conn, product_id: int, quantity: int):
        with conn.cursor() as cur:
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

    @staticmethod
    def update_order(
        conn,
        order_id: int,
        total_price: float,
    ):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
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

    @staticmethod
    def get_orders_paginated(
        conn,
        limit,
        offset,
        search,
        min_total,
        max_total,
        sort,
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

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

            query += (
                " ORDER BY created_at DESC"
                if sort == "desc"
                else " ORDER BY created_at ASC"
            )

            query += " LIMIT %s OFFSET %s"

            params.extend([limit, offset])

            cur.execute(query, params)

            return cur.fetchall()

    @staticmethod
    def count_orders(
        conn,
        search=None,
        min_total=None,
        max_total=None,
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

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
    # ORDERS
    # =====================================================

    @staticmethod
    def get_order_by_id(conn, order_id: int):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    total_price,
                    created_at
                FROM orders
                WHERE id=%s
                """,
                (order_id,),
            )

            return cur.fetchone()

    @staticmethod
    def get_orders_by_user(conn, user_id: int):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    user_id,
                    total_price,
                    created_at
                FROM orders
                WHERE user_id=%s
                ORDER BY created_at DESC
                """,
                (user_id,),
            )

            return cur.fetchall()

    @staticmethod
    def get_order_items(conn, order_id: int):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    product_id,
                    quantity,
                    price
                FROM order_items
                WHERE order_id=%s
                ORDER BY id
                """,
                (order_id,),
            )

            return cur.fetchall()

    # =====================================================
    # DELETE
    # =====================================================

    @staticmethod
    def delete_order_items(conn, order_id: int):
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM order_items
                WHERE order_id=%s
                """,
                (order_id,),
            )

    @staticmethod
    def delete_order(conn, order_id: int):
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM orders
                WHERE id=%s
                """,
                (order_id,),
            )