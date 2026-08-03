from fastapi import APIRouter, Depends, status

from app.core.security import admin_required
from app.dependencies.unit_of_work import get_uow
from app.schemas.inventory import (
    InventoryTransactionCreate,
    InventoryTransactionResponse,
    StockMovementResponse,
    InventoryTransactionReverse,
)
from app.services.inventory_service import InventoryService


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post(
    "/transactions",
    response_model=InventoryTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)],
)
def create_inventory_transaction(
    data: InventoryTransactionCreate,
    uow=Depends(get_uow),
):
    service = InventoryService(uow)

    return service.create_transaction(data)


@router.get(
    "/products/{product_id}/history",
    response_model=list[InventoryTransactionResponse],
)
def get_product_history(
    product_id: int,
    uow=Depends(get_uow),
):
    service = InventoryService(uow)

    return service.get_product_history(product_id)


@router.get(
    "/stock-movements",
    response_model=list[StockMovementResponse],
)
def get_stock_movements(
    uow=Depends(get_uow),
):
    service = InventoryService(uow)

    return service.get_stock_movements()


@router.post(
    "/transactions/{transaction_id}/reverse",
    response_model=InventoryTransactionResponse,
    dependencies=[Depends(admin_required)],
)
def reverse_inventory_transaction(
    transaction_id: int,
    data: InventoryTransactionReverse,
    uow=Depends(get_uow),
):
    service = InventoryService(uow)

    return service.reverse_transaction(
        transaction_id,
        data.note,
    )