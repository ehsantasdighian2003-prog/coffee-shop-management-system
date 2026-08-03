from psycopg2.extras import RealDictCursor


class SupplierRepository:
    """
    Repository responsible for supplier database operations.
    """

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================

    def create_supplier(
        self,
        name,
        phone=None,
        email=None,
        address=None,
    ):

        query = """
            INSERT INTO suppliers
            (
                name,
                phone,
                email,
                address
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (
                    name,
                    phone,
                    email,
                    address,
                ),
            )

            return cursor.fetchone()


    # =========================
    # GET BY ID
    # =========================

    def get_supplier_by_id(
        self,
        supplier_id: int,
    ):

        query = """
            SELECT *
            FROM suppliers
            WHERE id = %s
            AND is_deleted = FALSE
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (supplier_id,),
            )

            return cursor.fetchone()


    # =========================
    # LIST PAGINATED
    # =========================

    def get_suppliers_paginated(
        self,
        page,
        limit,
        search=None,
    ):

        offset = (page - 1) * limit

        query = """
            SELECT *
            FROM suppliers
            WHERE is_deleted = FALSE
        """

        params = []

        if search:

            query += """
                AND name ILIKE %s
            """

            params.append(
                f"%{search}%"
            )


        query += """
            ORDER BY id DESC
            LIMIT %s
            OFFSET %s
        """

        params.extend(
            [
                limit,
                offset,
            ]
        )

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                params,
            )

            return cursor.fetchall()


    # =========================
    # COUNT
    # =========================

    def count_suppliers(
        self,
        search=None,
    ):

        query = """
            SELECT COUNT(*)
            FROM suppliers
            WHERE is_deleted = FALSE
        """

        params = []

        if search:

            query += """
                AND name ILIKE %s
            """

            params.append(
                f"%{search}%"
            )


        with self.conn.cursor() as cursor:

            cursor.execute(
                query,
                params,
            )

            return cursor.fetchone()[0]


    # =========================
    # UPDATE
    # =========================

    def update_supplier(
        self,
        supplier_id,
        name,
        phone,
        email,
        address,
    ):

        query = """
            UPDATE suppliers
            SET
                name = COALESCE(%s, name),
                phone = COALESCE(%s, phone),
                email = COALESCE(%s, email),
                address = COALESCE(%s, address),
                updated_at = CURRENT_TIMESTAMP

            WHERE id = %s
            AND is_deleted = FALSE

            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (
                    name,
                    phone,
                    email,
                    address,
                    supplier_id,
                ),
            )

            return cursor.fetchone()


    # =========================
    # SOFT DELETE
    # =========================

    def delete_supplier(
        self,
        supplier_id,
    ):

        query = """
            UPDATE suppliers
            SET
                is_deleted = TRUE,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = %s
            AND is_deleted = FALSE

            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (supplier_id,),
            )

            return cursor.fetchone()


    # =========================
    # RESTORE
    # =========================

    def restore_supplier(
        self,
        supplier_id,
    ):

        query = """
            UPDATE suppliers
            SET
                is_deleted = FALSE,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = %s
            AND is_deleted = TRUE

            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (supplier_id,),
            )

            return cursor.fetchone()
        
        
    # =========================
    # ACTIVATE
    # =========================

    def activate_supplier(
        self,
        supplier_id,
    ):
        

        query = """
            UPDATE suppliers
            SET
                is_active = TRUE,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = %s
            AND is_deleted = FALSE

            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (supplier_id,),
            )

            return cursor.fetchone()


    # =========================
    # DEACTIVATE
    # =========================

    def deactivate_supplier(
        self,
        supplier_id,
    ):
        

        query = """
            UPDATE suppliers
            SET
                is_active = FALSE,
                updated_at = CURRENT_TIMESTAMP

            WHERE id = %s
            AND is_deleted = FALSE

            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (supplier_id,),
            )

            return cursor.fetchone()