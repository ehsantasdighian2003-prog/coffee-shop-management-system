from decimal import Decimal

from fastapi import HTTPException, status

from app.core.unit_of_work import UnitOfWork
from app.repositories.order_repository import OrderRepository


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


    def __init__(
        self,
        repo: OrderRepository | None = None
    ):
        self.repo = repo or OrderRepository()


    # =====================================================
    # PRIVATE HELPERS
    # =====================================================


    @staticmethod
    def _to_float(value):
        """
        Convert Decimal values
        into JSON compatible numbers.
        """

        if isinstance(value, Decimal):
            return float(value)

        return value



    def _serialize_order(
        self,
        order: dict
    ):
        """
        Normalize order object.
        """

        return {
            "id": order["id"],
            "user_id": order["user_id"],
            "total_price": self._to_float(
                order["total_price"]
            ),
            "created_at": order["created_at"]
        }



    def _serialize_item(
        self,
        item: dict
    ):
        """
        Normalize order item.
        """

        return {
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": self._to_float(
                item["price"]
            )
        }



    def _check_order_permission(
        self,
        order: dict,
        user: dict
    ):
        """
        Validate user access.

        Admin:
            Can access all orders.

        User:
            Can access own orders only.
        """

        is_admin = (
            user["role"] == "admin"
        )

        is_owner = (
            order["user_id"] == user["id"]
        )


        if not is_admin and not is_owner:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied."
            )



    def _validate_order_items(
        self,
        conn,
        items: list
    ):
        """
        Validate products and
        calculate order total.
        """

        validated_items = []

        total_price = Decimal("0")


        for item in items:

            product = self.repo.get_product_by_id(
                conn=conn,
                product_id=item.product_id
            )


            if not product:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found."
                )



            if not product["is_active"]:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {item.product_id} is inactive."
                )



            if product["stock"] < item.quantity:

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Not enough stock for product {item.product_id}."
                )



            price = product["price"]


            total_price += (
                price * item.quantity
            )


            validated_items.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": self._to_float(price)
                }
            )


        return (
            validated_items,
            total_price
        )



    def _build_order_result(
        self,
        order_id: int,
        user_id: int,
        total_price,
        items: list
    ):
        """
        Build order response.
        """

        return {
            "order_id": order_id,
            "user_id": user_id,
            "total_price": self._to_float(
                total_price
            ),
            "items": items
        }
        
    # =====================================================
    # ORDER ITEM HELPERS
    # =====================================================


    def _create_order_items(
        self,
        conn,
        order_id: int,
        items: list
    ):
        """
        Create order items and decrease stock.
        """

        for item in items:

            self.repo.create_order_item(
                conn=conn,
                order_id=order_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )


            self.repo.decrease_stock(
                conn=conn,
                product_id=item["product_id"],
                quantity=item["quantity"]
            )



    def _restore_order_stock(
        self,
        conn,
        items: list
    ):
        """
        Restore product stock
        from existing order items.
        """

        for item in items:

            self.repo.increase_stock(
                conn=conn,
                product_id=item["product_id"],
                quantity=item["quantity"]
            )



    # =====================================================
    # CREATE ORDER
    # =====================================================


    def create_order(
        self,
        user_id: int,
        items: list
    ):

        with UnitOfWork() as uow:

            validated_items, total_price = (
                self._validate_order_items(
                    conn=uow.conn,
                    items=items
                )
            )


            created_order = self.repo.create_order(
                conn=uow.conn,
                user_id=user_id,
                total_price=total_price
            )


            order_id = created_order["id"]


            self._create_order_items(
                conn=uow.conn,
                order_id=order_id,
                items=validated_items
            )


            return self._build_order_result(
                order_id=order_id,
                user_id=user_id,
                total_price=total_price,
                items=validated_items
            )



    # =====================================================
    # UPDATE ORDER
    # =====================================================


    def update_order(
        self,
        order_id: int,
        user: dict,
        items: list
    ):

        with UnitOfWork() as uow:

            order = self.repo.get_order_by_id(
                conn=uow.conn,
                order_id=order_id
            )


            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found."
                )


            self._check_order_permission(
                order,
                user
            )


            old_items = self.repo.get_order_items(
                conn=uow.conn,
                order_id=order_id
            )


            self._restore_order_stock(
                conn=uow.conn,
                items=old_items
            )


            self.repo.delete_order_items(
                conn=uow.conn,
                order_id=order_id
            )


            validated_items, total_price = (
                self._validate_order_items(
                    conn=uow.conn,
                    items=items
                )
            )


            self._create_order_items(
                conn=uow.conn,
                order_id=order_id,
                items=validated_items
            )


            self.repo.update_order(
                conn=uow.conn,
                order_id=order_id,
                total_price=total_price
            )


            return self._build_order_result(
                order_id=order_id,
                user_id=order["user_id"],
                total_price=total_price,
                items=validated_items
            )
            
    # =====================================================
    # DELETE ORDER
    # =====================================================


    def delete_order(
        self,
        order_id: int,
        user: dict
    ):

        with UnitOfWork() as uow:

            order = self.repo.get_order_by_id(
                conn=uow.conn,
                order_id=order_id
            )


            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found."
                )


            self._check_order_permission(
                order,
                user
            )


            items = self.repo.get_order_items(
                conn=uow.conn,
                order_id=order_id
            )


            self._restore_order_stock(
                conn=uow.conn,
                items=items
            )


            self.repo.delete_order_items(
                conn=uow.conn,
                order_id=order_id
            )


            self.repo.delete_order(
                conn=uow.conn,
                order_id=order_id
            )


            return {
                "message": "Order deleted successfully."
            }



    # =====================================================
    # GET ALL ORDERS
    # =====================================================


    def get_all_orders(
        self,
        user: dict,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        min_total: float | None = None,
        max_total: float | None = None,
        sort: str = "desc"
    ):


        if user["role"] != "admin":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin only access."
            )


        page = max(page, 1)

        limit = min(
            max(limit, 1),
            100
        )


        offset = (
            page - 1
        ) * limit


        with UnitOfWork() as uow:


            orders = self.repo.get_orders_paginated(
                conn=uow.conn,
                limit=limit,
                offset=offset,
                search=search,
                min_total=min_total,
                max_total=max_total,
                sort=sort
            )


            total = self.repo.count_orders(
                conn=uow.conn,
                search=search,
                min_total=min_total,
                max_total=max_total
            )


            pages = (
                total + limit - 1
            ) // limit


            return {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": pages,
                "data": [
                    self._serialize_order(order)
                    for order in orders
                ]
            }



    # =====================================================
    # GET ORDER BY ID
    # =====================================================


    def get_order_by_id(
        self,
        order_id: int,
        user: dict
    ):

        with UnitOfWork() as uow:


            order = self.repo.get_order_by_id(
                conn=uow.conn,
                order_id=order_id
            )


            if not order:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found."
                )


            self._check_order_permission(
                order,
                user
            )


            items = self.repo.get_order_items(
                conn=uow.conn,
                order_id=order_id
            )


            return {
                **self._serialize_order(order),
                "items": [
                    self._serialize_item(item)
                    for item in items
                ]
            }



    # =====================================================
    # GET MY ORDERS
    # =====================================================


    def get_orders_by_user(
        self,
        user_id: int
    ):

        with UnitOfWork() as uow:

            orders = self.repo.get_orders_by_user(
                conn=uow.conn,
                user_id=user_id
            )


            return [
                self._serialize_order(order)
                for order in orders
            ]