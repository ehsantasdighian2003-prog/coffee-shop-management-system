from typing import Optional

from psycopg2.extras import RealDictCursor


class PurchaseOrderRepository:

    def __init__(self, conn):
        self.conn = conn


    def create_purchase_order(self, data: dict):

        query = """
            INSERT INTO purchase_orders (
                supplier_id,
                status,
                total_amount,
                notes
            )
            VALUES (
                %s,
                %s,
                %s,
                %s
            )
            RETURNING *
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                query,
                (
                    data["supplier_id"],
                    data.get("status", "draft"),
                    data.get("total_amount", 0),
                    data.get("notes"),
                ),
            )

            return cur.fetchone()


    def get_purchase_order_by_id(self, purchase_order_id: int):

        query = """
            SELECT *
            FROM purchase_orders
            WHERE id = %s
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                query,
                (purchase_order_id,),
            )

            purchase_order = cur.fetchone()

        if not purchase_order:
            return None

        purchase_order["items"] = self.get_items(
            purchase_order_id
        )

        return purchase_order


    def get_all_purchase_orders(self):

        query = """
            SELECT *
            FROM purchase_orders
            ORDER BY created_at DESC
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(query)

            purchase_orders = cur.fetchall()

        for purchase_order in purchase_orders:
            purchase_order["items"] = self.get_items(
                purchase_order["id"]
            )

        return purchase_orders


    def update_status(
        self,
        purchase_order_id: int,
        status: str,
    ):

        query = """
            UPDATE purchase_orders
            SET status = %s,
                updated_at = NOW()
            WHERE id = %s
            RETURNING *
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                query,
                (
                    status,
                    purchase_order_id,
                ),
            )

            return cur.fetchone()


    def delete_purchase_order(self, purchase_order_id: int):
        pass


    def add_item(
        self,
        purchase_order_id: int,
        item: dict,
    ):

        total_price = (
            item["quantity"] *
            item["unit_price"]
        )

        query = """
            INSERT INTO purchase_order_items (
                purchase_order_id,
                product_id,
                quantity,
                unit_price,
                total_price
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING *
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                query,
                (
                    purchase_order_id,
                    item["product_id"],
                    item["quantity"],
                    item["unit_price"],
                    total_price,
                ),
            )

            return cur.fetchone()


    def get_items(self, purchase_order_id: int):

        query = """
            SELECT *
            FROM purchase_order_items
            WHERE purchase_order_id = %s
            ORDER BY id
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:

            cur.execute(
                query,
                (purchase_order_id,),
            )

            return cur.fetchall()
        