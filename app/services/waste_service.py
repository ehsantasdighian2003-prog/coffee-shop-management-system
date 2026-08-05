from app.core.unit_of_work import UnitOfWork
from app.core.exceptions import (
    ProductNotFoundException,
    ProductInactiveException,
    InsufficientStockException,
)


class WasteService:

    def __init__(
        self,
        uow: UnitOfWork,
    ):

        self.uow = uow


    # =========================
    # CREATE WASTE
    # =========================

    def create_waste(
        self,
        data: dict,
    ):

        # Get product
        product = (
            self.uow.inventory
            .get_product_by_id(
                data["product_id"]
            )
        )


        if product is None:

            raise ProductNotFoundException()


        if not product["is_active"]:

            raise ProductInactiveException()


        if product["stock"] < data["quantity"]:

            raise InsufficientStockException()


        # Decrease product stock

        self.uow.inventory.decrease_stock(
            data["product_id"],
            data["quantity"],
        )


        # Create inventory OUT transaction

        self.uow.inventory.create_transaction(
            product_id=data["product_id"],
            transaction_type="OUT",
            quantity=data["quantity"],
            note="waste",
        )


        # Create waste record

        waste = (
            self.uow.waste
            .create_waste(
                data
            )
        )


        self.uow.commit()


        return (
            self.uow.waste
            .get_waste_by_id(
                waste["id"]
            )
        )


    # =========================
    # GET BY ID
    # =========================

    def get_waste_by_id(
        self,
        waste_id: int,
    ):

        return (
            self.uow.waste
            .get_waste_by_id(
                waste_id
            )
        )


    # =========================
    # PRODUCT WASTE
    # =========================

    def get_product_waste(
        self,
        product_id: int,
    ):

        return (
            self.uow.waste
            .get_product_waste(
                product_id
            )
        )


    # =========================
    # WASTE REPORT
    # =========================

    def get_waste_report(self):

        return (
            self.uow.waste
            .get_waste_report()
        )