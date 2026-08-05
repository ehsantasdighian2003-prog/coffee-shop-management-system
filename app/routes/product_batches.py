from fastapi import APIRouter, Query

from app.core.unit_of_work import UnitOfWork
from app.schemas.product_batch import (
    ProductBatchCreate,
    ProductBatchDetailResponse,
    ProductBatchResponse,
)
from app.services.product_batch_service import ProductBatchService


router = APIRouter(
    prefix="/product-batches",
    tags=["Product Batches"],
)


# =========================
# CREATE BATCH
# =========================

@router.post(
    "",
    response_model=ProductBatchResponse,
    status_code=201,
)
def create_batch(
    payload: ProductBatchCreate,
):

    uow = UnitOfWork()

    with uow:

        service = ProductBatchService(uow)

        return service.create_batch(
            payload.model_dump()
        )


# =========================
# EXPIRING BATCHES
# =========================

@router.get(
    "/expiring",
)
def get_expiring_batches(
    days: int = Query(
        30,
        ge=1,
    ),
):

    uow = UnitOfWork()

    with uow:

        service = ProductBatchService(uow)

        return service.get_expiring_batches(
            days
        )


# =========================
# PRODUCT BATCHES
# =========================

@router.get(
    "/product/{product_id}",
)
def get_product_batches(
    product_id: int,
):

    uow = UnitOfWork()

    with uow:

        service = ProductBatchService(uow)

        return service.get_product_batches(
            product_id
        )


# =========================
# GET BATCH BY ID
# =========================

@router.get(
    "/{batch_id}",
    response_model=ProductBatchDetailResponse,
)
def get_batch(
    batch_id: int,
):

    uow = UnitOfWork()

    with uow:

        service = ProductBatchService(uow)

        return service.get_batch_by_id(
            batch_id
        )