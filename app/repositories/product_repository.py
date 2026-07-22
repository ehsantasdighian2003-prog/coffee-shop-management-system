from psycopg2.extras import RealDictCursor


class ProductRepository:


    def __init__(self, conn):

        self.conn = conn



    # =========================
    # BASE PRODUCT SELECT
    # =========================

    PRODUCT_SELECT = """
        SELECT
            products.id,
            products.name,
            products.description,
            products.price,
            products.stock,
            products.is_active,

            CASE
                WHEN categories.id IS NOT NULL
                THEN json_build_object(
                    'id',
                    categories.id,
                    'name',
                    categories.name
                )
                ELSE NULL
            END AS category

        FROM products

        LEFT JOIN categories
        ON products.category_id = categories.id
    """



    # =========================
    # CREATE PRODUCT
    # =========================

    def create_product(
        self,
        name,
        description,
        price,
        stock,
        is_active,
        category_id
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                INSERT INTO products(
                    name,
                    description,
                    price,
                    stock,
                    is_active,
                    category_id
                )

                VALUES (%s,%s,%s,%s,%s,%s)

                RETURNING id
                """,
                (
                    name,
                    description,
                    price,
                    stock,
                    is_active,
                    category_id
                )
            )


            product_id = cur.fetchone()["id"]


            cur.execute(
                self.PRODUCT_SELECT +
                """
                WHERE products.id = %s
                """,
                (product_id,)
            )


            return cur.fetchone()



    # =========================
    # GET PRODUCTS PAGINATED
    # =========================

    def get_products_paginated(
        self,
        page,
        limit,
        category_id=None,
        search=None,
        sort=None
    ):

        offset = (page - 1) * limit

        query = self.PRODUCT_SELECT

        conditions = []
        params = []


        if category_id:

            conditions.append(
                "products.category_id = %s"
            )

            params.append(category_id)



        if search:

            conditions.append(
                """
                (
                    products.name ILIKE %s
                    OR products.description ILIKE %s
                )
                """
            )

            params.extend(
                [
                    f"%{search}%",
                    f"%{search}%"
                ]
            )



        if conditions:

            query += (
                " WHERE "
                +
                " AND ".join(conditions)
            )



        if sort == "price_asc":

            query += """
                ORDER BY products.price ASC
            """


        elif sort == "price_desc":

            query += """
                ORDER BY products.price DESC
            """


        else:

            query += """
                ORDER BY products.id DESC
            """



        query += """
            LIMIT %s
            OFFSET %s
        """


        params.extend(
            [
                limit,
                offset
            ]
        )


        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                query,
                params
            )

            return cur.fetchall()



    # =========================
    # COUNT PRODUCTS
    # =========================

    def count_products(
        self,
        category_id=None,
        search=None
    ):

        query = """
            SELECT COUNT(*)
            FROM products
        """


        conditions = []
        params = []



        if category_id:

            conditions.append(
                "category_id = %s"
            )

            params.append(category_id)



        if search:

            conditions.append(
                """
                (
                    name ILIKE %s
                    OR description ILIKE %s
                )
                """
            )

            params.extend(
                [
                    f"%{search}%",
                    f"%{search}%"
                ]
            )



        if conditions:

            query += (
                " WHERE "
                +
                " AND ".join(conditions)
            )



        with self.conn.cursor() as cur:

            cur.execute(
                query,
                params
            )

            return cur.fetchone()[0]



    # =========================
    # GET PRODUCT BY ID
    # =========================

    def get_product_by_id(
        self,
        product_id
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                self.PRODUCT_SELECT +
                """
                WHERE products.id = %s
                """,
                (product_id,)
            )

            return cur.fetchone()



    # =========================
    # UPDATE PRODUCT
    # =========================

    def update_product(
        self,
        product_id,
        name,
        description,
        price,
        stock,
        is_active,
        category_id
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:


            cur.execute(
                """
                UPDATE products

                SET
                    name = COALESCE(%s, name),
                    description = COALESCE(%s, description),
                    price = COALESCE(%s, price),
                    stock = COALESCE(%s, stock),
                    is_active = COALESCE(%s, is_active),
                    category_id = COALESCE(%s, category_id)

                WHERE id = %s

                RETURNING id
                """,
                (
                    name,
                    description,
                    price,
                    stock,
                    is_active,
                    category_id,
                    product_id
                )
            )


            updated = cur.fetchone()


            if not updated:

                return None



            cur.execute(
                self.PRODUCT_SELECT +
                """
                WHERE products.id = %s
                """,
                (product_id,)
            )


            return cur.fetchone()



    # =========================
    # DELETE PRODUCT
    # =========================

    def delete_product(
        self,
        product_id
    ):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                """
                DELETE FROM products

                WHERE id = %s

                RETURNING id
                """,
                (product_id,)
            )


            return cur.fetchone()
