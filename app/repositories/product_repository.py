from psycopg2.extras import RealDictCursor


class ProductRepository:


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

    @staticmethod
    def create_product(
        conn,
        name,
        description,
        price,
        stock,
        is_active,
        category_id
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

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
                ProductRepository.PRODUCT_SELECT +
                """
                WHERE products.id = %s
                """,
                (product_id,)
            )

            return cur.fetchone()



    # =========================
    # GET PRODUCTS PAGINATED
    # =========================

    @staticmethod
    def get_products_paginated(
        conn,
        page,
        limit,
        category_id=None,
        search=None,
        sort=None
    ):

        offset = (page - 1) * limit

        query = ProductRepository.PRODUCT_SELECT

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

            query += " WHERE " + " AND ".join(conditions)



        if sort == "price_asc":

            query += " ORDER BY products.price ASC"


        elif sort == "price_desc":

            query += " ORDER BY products.price DESC"


        else:

            query += " ORDER BY products.id DESC"



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


        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                query,
                params
            )

            return cur.fetchall()



    # =========================
    # COUNT PRODUCTS
    # =========================

    @staticmethod
    def count_products(
        conn,
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


        with conn.cursor() as cur:

            cur.execute(
                query,
                params
            )

            return cur.fetchone()[0]



    # =========================
    # GET PRODUCT BY ID
    # =========================

    @staticmethod
    def get_product_by_id(
        conn,
        product_id
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                ProductRepository.PRODUCT_SELECT +
                """
                WHERE products.id = %s
                """,
                (product_id,)
            )

            return cur.fetchone()



    # =========================
    # DELETE PRODUCT
    # =========================

    @staticmethod
    def delete_product(
        conn,
        product_id
    ):

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                """
                DELETE FROM products
                WHERE id = %s
                RETURNING id
                """,
                (product_id,)
            )

            return cur.fetchone()
