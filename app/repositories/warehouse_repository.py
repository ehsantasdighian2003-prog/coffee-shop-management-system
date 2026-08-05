from psycopg2.extras import RealDictCursor


class WarehouseRepository:

    def __init__(self, conn):
        self.conn = conn


    # =========================
    # CREATE WAREHOUSE
    # =========================

    def create_warehouse(
        self,
        name,
        location=None,
    ):

        query = """
            INSERT INTO warehouses
            (
                name,
                location
            )
            VALUES
            (
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
                    location,
                ),
            )

            return cursor.fetchone()


    # =========================
    # GET WAREHOUSE BY ID
    # =========================

    def get_warehouse_by_id(
        self,
        warehouse_id,
    ):

        query = """
            SELECT *
            FROM warehouses
            WHERE id = %s
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (warehouse_id,),
            )

            return cursor.fetchone()


    # =========================
    # GET ALL WAREHOUSES
    # =========================

    def get_all_warehouses(self):

        query = """
            SELECT *
            FROM warehouses
            ORDER BY id DESC
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(query)

            return cursor.fetchall()


    # =========================
    # ADD PRODUCT TO WAREHOUSE
    # =========================

    def add_product(
        self,
        warehouse_id,
        product_id,
        quantity,
    ):

        query = """
            INSERT INTO warehouse_inventory
            (
                warehouse_id,
                product_id,
                quantity
            )
            VALUES
            (
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
                    warehouse_id,
                    product_id,
                    quantity,
                ),
            )

            return cursor.fetchone()


    # =========================
    # GET WAREHOUSE INVENTORY
    # =========================

    def get_inventory(
        self,
        warehouse_id,
    ):

        query = """
            SELECT
                wi.id,
                wi.warehouse_id,
                wi.product_id,
                p.name AS product_name,
                wi.quantity

            FROM warehouse_inventory wi

            JOIN products p
            ON p.id = wi.product_id

            WHERE wi.warehouse_id = %s

            ORDER BY wi.id
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (warehouse_id,),
            )

            return cursor.fetchall()