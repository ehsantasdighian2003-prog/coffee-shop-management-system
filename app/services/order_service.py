from decimal import Decimal

from fastapi import HTTPException, status

from app.core.unit_of_work import UnitOfWork


class OrderService:
    """
    Handles order business logic.

    Responsibilities:
    - Order creation
    - Order update
    - Order deletion
    - Stock management
    - Permission validation
    """

    def __init__(self):
        pass

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    @staticmethod
    def _to_float(value):

        if isinstance(value, Decimal):
            return float(value)

        return value

    def _serialize_order(self, order: dict):

        return {
            "id": order["id"],
            "user_id": order["user_id"],
            "total_price": self._to_float(order["total_price"]),
            "created_at": order["created_at"],
        }

    def _serialize_item(self, item: dict):

        return {
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": self._to_float(item["price"]),
        }

    def _check_order_permission(self, order: dict, user: dict):

        is_admin = user["role"] == "admin"

        is_owner = order["user_id"] == user["id"]

        if not is_admin and not is_owner:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied."
            )

    def _validate_order_items(self, uow, items: list):

        validated_items = []

        total_price = Decimal("0")

        for item in items:

            product = uow.orders.get_product_by_id(product_id=item.product_id)

            if not product:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found.",
                )

            if not product["is_active"]:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {item.product_id} is inactive.",
                )

            if product["stock"] < item.quantity:

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Not enough stock for product {item.product_id}.",
                )

            price = product["price"]

            total_price += price * item.quantity

            validated_items.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": price,
                }
            )

        return (validated_items, total_price)

    def _build_order_result(
        self, order_id: int, user_id: int, total_price, items: list
    ):

        return {
            "order_id": order_id,
            "user_id": user_id,
            "total_price": self._to_float(total_price),
            "items": items,
        }

    # =====================================================
    # ORDER ITEMS
    # =====================================================

    def _create_order_items(self, uow, order_id: int, items: list):

        for item in items:

            uow.orders.create_order_item(
                order_id=order_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
            )

            uow.orders.decrease_stock(
                product_id=item["product_id"], quantity=item["quantity"]
            )

    def _restore_order_stock(self, uow, items: list):

        for item in items:

            uow.orders.increase_stock(
                product_id=item["product_id"], quantity=item["quantity"]
            )

    # =====================================================
    # CREATE
    # =====================================================

    def create_order(self, user_id: int, items: list):

        with UnitOfWork() as uow:

            validated_items, total_price = self._validate_order_items(uow, items)

            created_order = uow.orders.create_order(
                user_id=user_id, total_price=total_price
            )

            order_id = created_order["id"]

            self._create_order_items(uow, order_id, validated_items)

            return self._build_order_result(
                order_id, user_id, total_price, validated_items
            )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_order(self, order_id: int, user: dict, items: list):

        with UnitOfWork() as uow:

            order = uow.orders.get_order_by_id(order_id)

            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found."
                )

            self._check_order_permission(order, user)

            old_items = uow.orders.get_order_items(order_id)

            self._restore_order_stock(uow, old_items)

            uow.orders.delete_order_items(order_id)

            validated_items, total_price = self._validate_order_items(uow, items)

            self._create_order_items(uow, order_id, validated_items)

            uow.orders.update_order(order_id, total_price)

            return self._build_order_result(
                order_id, order["user_id"], total_price, validated_items
            )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_order(self, order_id: int, user: dict):

        with UnitOfWork() as uow:

            order = uow.orders.get_order_by_id(order_id)

            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found."
                )

            self._check_order_permission(order, user)

            items = uow.orders.get_order_items(order_id)

            self._restore_order_stock(uow, items)

            uow.orders.delete_order_items(order_id)

            uow.orders.delete_order(order_id)

            return {"message": "Order deleted successfully."}

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all_orders(
        self,
        user: dict,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        min_total: float | None = None,
        max_total: float | None = None,
        sort: str = "desc",
    ):

        if user["role"] != "admin":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Admin only access."
            )

        page = max(page, 1)

        limit = min(max(limit, 1), 100)

        offset = (page - 1) * limit

        with UnitOfWork() as uow:

            orders = uow.orders.get_orders_paginated(
                limit, offset, search, min_total, max_total, sort
            )

            total = uow.orders.count_orders(search, min_total, max_total)

            pages = (total + limit - 1) // limit

            return {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": pages,
                "data": [self._serialize_order(order) for order in orders],
            }

    # =====================================================
    # GET BY ID
    # =====================================================

    def get_order_by_id(self, order_id: int, user: dict):

        with UnitOfWork() as uow:

            order = uow.orders.get_order_by_id(order_id)

            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found."
                )

            self._check_order_permission(order, user)

            items = uow.orders.get_order_items(order_id)

            return {
                **self._serialize_order(order),
                "items": [self._serialize_item(item) for item in items],
            }

    # =====================================================
    # MY ORDERS
    # =====================================================

    def get_orders_by_user(self, user_id: int):

        with UnitOfWork() as uow:

            orders = uow.orders.get_orders_by_user(user_id)

            return [self._serialize_order(order) for order in orders]
        
        
    # =====================================================
    # UPDATE ORDER STATUS
    # =====================================================

    def update_order_status(
        self,
        order_id: int,
        status: str,
        user: dict,
    ):

        if user["role"] != "admin":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin only access.",
            )

        with UnitOfWork() as uow:

            order = uow.orders.get_order_by_id(order_id)

            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found.",
                )

            updated = uow.orders.update_order_status(
                order_id,
                status,
            )

            uow.orders.add_status_history(
                order_id=order_id,
                status=status,
                changed_by=user["id"],
            )

            return updated
        
        
    # =====================================================
    # GET ORDER STATUS HISTORY
    # =====================================================

    def get_order_status_history(
        self,
        order_id: int,
        user: dict,
    ):

        with UnitOfWork() as uow:

            order = uow.orders.get_order_by_id(order_id)

            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found.",
                )

            self._check_order_permission(order, user)

            return uow.orders.get_order_status_history(order_id)
        