from app.core.unit_of_work import UnitOfWork


class InventoryReportService:
    """
    Service layer for inventory reports.
    """

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow


    # =========================
    # STOCK SUMMARY
    # =========================

    def get_stock_summary(self):


        return (
            self.uow.inventory_report
            .get_stock_summary()
        )


    # =========================
    # INVENTORY MOVEMENTS
    # =========================

    def get_inventory_movements(self):

        return (
            self.uow.inventory_report
            .get_inventory_movements()
        )


    # =========================
    # WASTE COST REPORT
    # =========================

    def get_waste_cost_report(self):

        return (
            self.uow.inventory_report
            .get_waste_cost_report()
        )


    # =========================
    # WAREHOUSE STOCK
    # =========================

    def get_warehouse_stock_report(self):

        return (
            self.uow.inventory_report
            .get_warehouse_stock_report()
        )


    # =========================
    # EXPIRING BATCHES
    # =========================

    def get_expiring_batches(
        self,
        days: int = 30,
    ):

        return (
            self.uow.inventory_report
            .get_expiring_batches(
                days
            )
        )