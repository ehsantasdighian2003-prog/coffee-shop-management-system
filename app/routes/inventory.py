from fastapi import APIRouter, Depends, status

from app.core.security import admin_required
from app.dependencies.unit_of_work import get_uow
from app.schemas.inventory import (
    InventoryTransactionCreate,
    InventoryTransactionResponse,
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