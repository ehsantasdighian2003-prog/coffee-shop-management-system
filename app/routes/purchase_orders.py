from fastapi import APIRouter, Depends

from app.core.unit_of_work import UnitOfWork
from app.services.purchase_order_service import PurchaseOrderService
from app.schemas.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderResponse,
)


router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
)


def get_service():

    uow = UnitOfWork()

    uow.__enter__()

    return PurchaseOrderService(uow)

@router.post(
    "",
    response_model=PurchaseOrderResponse,
)
def create_purchase_order(
    payload: PurchaseOrderCreate,
    service: PurchaseOrderService = Depends(get_service),
):

    return service.create_purchase_order(
        payload.model_dump()
    )
    
    
@router.put(
    "/{purchase_order_id}/receive",
    response_model=PurchaseOrderResponse,
)
def receive_purchase_order(
    purchase_order_id: int,
    service: PurchaseOrderService = Depends(get_service),
):

    return service.receive_purchase_order(
        purchase_order_id
    )