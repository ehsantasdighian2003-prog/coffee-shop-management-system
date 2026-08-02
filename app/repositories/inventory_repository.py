class InventoryRepository:
    """
    Repository responsible for inventory transaction operations.
    """

    def __init__(self, conn):
        self.conn = conn

    def create_transaction(
        self,
        product_id,
        transaction_type,
        quantity,
        note=None,
    ):
        query = """
            INSERT INTO inventory_transactions
            (
                product_id,
                transaction_type,
                quantity,
                note
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

        with self.conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    product_id,
                    transaction_type,
                    quantity,
                    note,
                ),
            )

            return cursor.fetchone()