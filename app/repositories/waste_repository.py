from psycopg2.extras import RealDictCursor


class WasteRepository:

    def __init__(self, conn):

        self.conn = conn


    # =========================
    # CREATE WASTE RECORD
    # =========================

    def create_waste(
        self,
        data: dict,
    ):

        query = """
            INSERT INTO waste_records
            (
                product_id,
                warehouse_id,
                quantity,
                reason,
                cost,
                created_by
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
                    data["quantity"],
                    data["reason"],
                    data.get("cost", 0),
                    data.get("created_by"),
                ),
            )

            return cursor.fetchone()



    # =========================
    # GET BY ID
    # =========================

    def get_waste_by_id(
        self,
        waste_id: int,
    ):

        query = """
            SELECT
                wr.*,
                p.name AS product_name,
                w.name AS warehouse_name

            FROM waste_records wr

            JOIN products p
                ON wr.product_id = p.id

            JOIN warehouses w
                ON wr.warehouse_id = w.id

            WHERE wr.id = %s
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (waste_id,),
            )

            return cursor.fetchone()



    # =========================
    # PRODUCT WASTE HISTORY
    # =========================

    def get_product_waste(
        self,
        product_id: int,
    ):

        query = """
            SELECT
                wr.*,
                p.name AS product_name,
                w.name AS warehouse_name

            FROM waste_records wr

            JOIN products p
                ON wr.product_id = p.id

            JOIN warehouses w
                ON wr.warehouse_id = w.id

            WHERE wr.product_id = %s

            ORDER BY wr.created_at DESC
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
    # WASTE REPORT
    # =========================

    def get_waste_report(self):

        query = """
            SELECT
                p.id AS product_id,
                p.name AS product_name,

                SUM(wr.quantity) AS total_quantity,

                SUM(wr.cost) AS total_cost

            FROM waste_records wr

            JOIN products p
                ON wr.product_id = p.id

            GROUP BY
                p.id,
                p.name

            ORDER BY total_cost DESC
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(query)

            return cursor.fetchall()