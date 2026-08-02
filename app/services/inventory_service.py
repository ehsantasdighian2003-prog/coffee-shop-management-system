class InventoryService:
    """
    Service responsible for inventory operations.
    """

    def __init__(self, uow):
        self.uow = uow

    def create_transaction(self, data):
        transaction = self.uow.inventory.create_transaction(
            product_id=data.product_id,
            transaction_type=data.transaction_type,
            quantity=data.quantity,
            note=data.note,
        )

        self.uow.commit()

        return transaction