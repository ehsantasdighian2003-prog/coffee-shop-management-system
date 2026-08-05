from app.core.unit_of_work import UnitOfWork


class PurchaseOrderService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow


    def create_purchase_order(
        self,
        data: dict,
    ):

        total_amount = 0

        for item in data["items"]:
            total_amount += (
                item["quantity"] *
                item["unit_price"]
            )


        purchase_order = (
            self.uow.purchase_order
            .create_purchase_order(
                {
                    "supplier_id": data["supplier_id"],
                    "notes": data.get("notes"),
                    "total_amount": total_amount,
                }
            )
        )


        for item in data["items"]:

            self.uow.purchase_order.add_item(
                purchase_order["id"],
                item,
            )


        self.uow.commit()


        return (
            self.uow.purchase_order
            .get_purchase_order_by_id(
                purchase_order["id"]
            )
        )


    def get_purchase_order_by_id(
        self,
        purchase_order_id: int,
    ):

        return (
            self.uow.purchase_order
            .get_purchase_order_by_id(
                purchase_order_id
            )
        )


    def get_all_purchase_orders(self):

        return (
            self.uow.purchase_order
            .get_all_purchase_orders()
        )
        

    def receive_purchase_order(
        self,
        purchase_order_id: int,
    ):

        purchase_order = (
            self.uow.purchase_order
            .get_purchase_order_by_id(
                purchase_order_id
            )
        )

        if not purchase_order:
            return None


        for item in purchase_order["items"]:

            self.uow.products.update_stock(
                item["product_id"],
                item["quantity"],
            )


            self.uow.inventory.create_transaction(
                {
                    "product_id": item["product_id"],
                    "change_type": "IN",
                    "quantity": item["quantity"],
                    "reason": "purchase_order_received",
                    "supplier_id": purchase_order["supplier_id"],
                    "order_id": purchase_order["id"],
                }
            )


        self.uow.purchase_order.update_status(
            purchase_order_id,
            "received",
        )


        self.uow.commit()


        return (
            self.uow.purchase_order
            .get_purchase_order_by_id(
                purchase_order_id
            )
        )
        
        
        
    def receive_purchase_order(
        self,
        purchase_order_id: int,
    ):

        purchase_order = (
            self.uow.purchase_order
            .get_purchase_order_by_id(
                purchase_order_id
            )
        )

        if not purchase_order:
            return None


        if purchase_order["status"] == "received":
            return purchase_order


        for item in purchase_order["items"]:

            product = (
                self.uow.inventory
                .get_product_by_id(
                    item["product_id"]
                )
            )

            if not product:
                continue


            new_stock = (
                product["stock"]
                +
                item["quantity"]
            )


            self.uow.inventory.update_product_stock(
                item["product_id"],
                new_stock,
            )


            self.uow.inventory.create_transaction(
                item["product_id"],
                "IN",
                item["quantity"],
                note="purchase_order_received",
                supplier_id=purchase_order["supplier_id"],
                purchase_order_id=purchase_order["id"],
            )


        self.uow.purchase_order.update_status(
            purchase_order_id,
            "received",
        )


        self.uow.commit()


        return (
            self.uow.purchase_order
            .get_purchase_order_by_id(
                purchase_order_id
            )
        )