from typing import Literal

from fastapi import APIRouter, Depends, Query, status

from app.core.security import get_current_user
from app.schemas.order import (
    OrderCreate,
    OrderDetail,
    OrderResponse,
    OrderSummary,
    OrderUpdate,
    PaginatedOrdersResponse,
)
from app.services.order_service import OrderService
from app.schemas.order import OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


order_service = OrderService()


# =====================================================
# CREATE ORDER
# =====================================================


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(request: OrderCreate, current_user: dict = Depends(get_current_user)):

    result = order_service.create_order(user_id=current_user["id"], items=request.items)

    return OrderResponse(**result)


# =====================================================
# UPDATE ORDER
# =====================================================


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int, request: OrderUpdate, current_user: dict = Depends(get_current_user)
):

    result = order_service.update_order(
        order_id=order_id, user=current_user, items=request.items
    )

    return OrderResponse(**result)


# =====================================================
# DELETE ORDER
# =====================================================


@router.delete("/{order_id}")
def delete_order(order_id: int, current_user: dict = Depends(get_current_user)):

    return order_service.delete_order(order_id=order_id, user=current_user)


# =====================================================
# GET ALL ORDERS
# =====================================================


@router.get("/", response_model=PaginatedOrdersResponse)
def get_all_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    min_total: float | None = Query(None, ge=0),
    max_total: float | None = Query(None, ge=0),
    sort: Literal["asc", "desc"] = "desc",
    current_user: dict = Depends(get_current_user),
):

    return order_service.get_all_orders(
        user=current_user,
        page=page,
        limit=limit,
        search=search,
        min_total=min_total,
        max_total=max_total,
        sort=sort,
    )


# =====================================================
# GET MY ORDERS
# =====================================================


@router.get("/me", response_model=list[OrderSummary])
def get_my_orders(current_user: dict = Depends(get_current_user)):

    return order_service.get_orders_by_user(current_user["id"])


# =====================================================
# GET ORDER BY ID
# =====================================================


@router.get("/{order_id}", response_model=OrderDetail)
def get_order_by_id(order_id: int, current_user: dict = Depends(get_current_user)):

    return order_service.get_order_by_id(order_id, current_user)


# =====================================================
# UPDATE ORDER STATUS
# =====================================================


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    request: OrderStatusUpdate,
    current_user: dict = Depends(get_current_user),
):

    return order_service.update_order_status(
        order_id=order_id,
        status=request.status,
        user=current_user,
    )


# =====================================================
# GET ORDER STATUS HISTORY
# =====================================================


@router.get("/{order_id}/history")
def get_order_status_history(
    order_id: int,
    current_user: dict = Depends(get_current_user),
):

    return order_service.get_order_status_history(
        order_id=order_id,
        user=current_user,
    )
