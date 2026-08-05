from app.core.unit_of_work import UnitOfWork


class ProductBatchService:

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow


    # =========================
    # CREATE BATCH
    # =========================

    def create_batch(
        self,
        data: dict,
    ):

        batch = (
            self.uow.product_batches
            .create_batch(
                data
            )
        )

        self.uow.commit()

        return batch


    # =========================
    # GET BY ID
    # =========================

    def get_batch_by_id(
        self,
        batch_id: int,
    ):

        return (
            self.uow.product_batches
            .get_batch_by_id(
                batch_id
            )
        )


    # =========================
    # PRODUCT BATCHES
    # =========================

    def get_product_batches(
        self,
        product_id: int,
    ):

        return (
            self.uow.product_batches
            .get_product_batches(
                product_id
            )
        )


    # =========================
    # EXPIRING BATCHES
    # =========================

    def get_expiring_batches(
        self,
        days: int = 30,
    ):

        return (
            self.uow.product_batches
            .get_expiring_batches(
                days
            )
        )