from psycopg2.extras import RealDictCursor


class ProductBatchRepository:

    def __init__(self, conn):
        self.conn = conn


    # =========================
    # CREATE BATCH
    # =========================

    def create_batch(
        self,
        data: dict,
    ):

        query = """
            INSERT INTO product_batches
            (
                product_id,
                warehouse_id,
                batch_number,
                quantity,
                production_date,
                expiration_date
            )
            VALUES
            (
                %s,
                %s,
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
                    data["product_id"],
                    data["warehouse_id"],
                    data["batch_number"],
                    data["quantity"],
                    data.get("production_date"),
                    data["expiration_date"],
                ),
            )

            return cursor.fetchone()


    # =========================
    # GET BATCH BY ID
    # =========================

    def get_batch_by_id(
        self,
        batch_id: int,
    ):

        query = """
            SELECT
                pb.*,
                p.name AS product_name,
                w.name AS warehouse_name

            FROM product_batches pb

            JOIN products p
            ON p.id = pb.product_id

            JOIN warehouses w
            ON w.id = pb.warehouse_id

            WHERE pb.id = %s
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (batch_id,),
            )

            return cursor.fetchone()


    # =========================
    # GET PRODUCT BATCHES
    # =========================

    def get_product_batches(
        self,
        product_id: int,
    ):

        query = """
            SELECT
                pb.*,
                p.name AS product_name,
                w.name AS warehouse_name

            FROM product_batches pb

            JOIN products p
            ON p.id = pb.product_id

            JOIN warehouses w
            ON w.id = pb.warehouse_id

            WHERE pb.product_id = %s

            ORDER BY pb.expiration_date
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (product_id,),
            )

            return cursor.fetchall()


    # =========================
    # EXPIRING SOON
    # =========================

    def get_expiring_batches(
        self,
        days: int,
    ):

        query = """
            SELECT
                pb.*,
                p.name AS product_name,
                w.name AS warehouse_name

            FROM product_batches pb

            JOIN products p
            ON p.id = pb.product_id

            JOIN warehouses w
            ON w.id = pb.warehouse_id

            WHERE pb.expiration_date
            <= CURRENT_DATE + %s

            ORDER BY pb.expiration_date
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (days,),
            )

            return cursor.fetchall()