from fastapi import HTTPException, status

from app.schemas.inventory import InventoryTransactionCreate


class InventoryService:
    """
    Service responsible for inventory operations.
    """

    def __init__(self, uow):
        self.uow = uow

    # ==================================================
    # CREATE INVENTORY TRANSACTION
    # ==================================================

    def create_transaction(
        self,
        data: InventoryTransactionCreate,
    ):

        product = self.uow.inventory.get_product_by_id(
            data.product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        current_stock = product["stock"] or 0

        if data.transaction_type == "IN":

            new_stock = current_stock + data.quantity

        elif data.transaction_type == "OUT":

            if current_stock < data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Not enough stock.",
                )

            new_stock = current_stock - data.quantity

        else:
            new_stock = data.quantity

        self.uow.inventory.update_product_stock(
            product_id=data.product_id,
            stock=new_stock,
        )

        transaction = self.uow.inventory.create_transaction(
            product_id=data.product_id,
            transaction_type=data.transaction_type,
            quantity=data.quantity,
            supplier_id=data.supplier_id,
            order_id=data.order_id,
            note=data.note,
        )

        self.uow.commit()

        return transaction


    # ==================================================
    # PRODUCT HISTORY
    # ==================================================

    def get_product_history(
        self,
        product_id: int,
    ):

        return self.uow.inventory.get_product_history(
            product_id
        )


    # ==================================================
    # STOCK MOVEMENTS
    # ==================================================

    def get_stock_movements(self):

        return self.uow.inventory.get_stock_movements()


    # ==================================================
    # REVERSE TRANSACTION
    # ==================================================

    def reverse_transaction(
        self,
        transaction_id: int,
        note: str | None = None,
    ):

        transaction = self.uow.inventory.get_transaction_by_id(
            transaction_id
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found.",
            )


        reverse_type = {
            "IN": "OUT",
            "OUT": "IN",
            "ADJUSTMENT": "ADJUSTMENT",
        }[transaction["change_type"]]


        reverse_data = InventoryTransactionCreate(
            product_id=transaction["product_id"],
            transaction_type=reverse_type,
            quantity=transaction["quantity"],
            supplier_id=transaction.get("supplier_id"),
            order_id=transaction.get("order_id"),
            note=note or f"Reverse transaction #{transaction_id}",
        )


        return self.create_transaction(
            reverse_data
        )
