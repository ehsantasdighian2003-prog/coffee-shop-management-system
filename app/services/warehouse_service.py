from app.core.unit_of_work import UnitOfWork


class WarehouseService:

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow


    # =========================
    # CREATE WAREHOUSE
    # =========================

    def create_warehouse(
        self,
        data: dict,
    ):

        warehouse = (
            self.uow.warehouses
            .create_warehouse(
                data["name"],
                data.get("location"),
            )
        )

        self.uow.commit()

        return warehouse


    # =========================
    # GET WAREHOUSE
    # =========================

    def get_warehouse_by_id(
        self,
        warehouse_id: int,
    ):

        return (
            self.uow.warehouses
            .get_warehouse_by_id(
                warehouse_id
            )
        )


    # =========================
    # GET ALL
    # =========================

    def get_all_warehouses(self):

        return (
            self.uow.warehouses
            .get_all_warehouses()
        )


    # =========================
    # ADD PRODUCT
    # =========================

    def add_product(
        self,
        warehouse_id: int,
        data: dict,
    ):

        result = (
            self.uow.warehouses
            .add_product(
                warehouse_id,
                data["product_id"],
                data["quantity"],
            )
        )

        self.uow.commit()

        return result


    # =========================
    # INVENTORY
    # =========================

    def get_inventory(
        self,
        warehouse_id: int,
    ):

        return (
            self.uow.warehouses
            .get_inventory(
                warehouse_id
            )
        )