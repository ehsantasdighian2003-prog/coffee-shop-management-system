from fastapi import APIRouter

from app.core.unit_of_work import UnitOfWork
from app.schemas.waste import (
    WasteCreate,
    WasteDetailResponse,
    WasteReportResponse,
)
from app.services.waste_service import WasteService


router = APIRouter(
    prefix="/waste",
    tags=["Waste Management"],
)


# =========================
# CREATE WASTE
# =========================

@router.post(
    "",
    response_model=WasteDetailResponse,
    status_code=201,
)
def create_waste(
    payload: WasteCreate,
):

    uow = UnitOfWork()

    with uow:

        service = WasteService(uow)

        return service.create_waste(
            payload.model_dump()
        )


# =========================
# WASTE REPORT
# =========================

@router.get(
    "/report",
    response_model=list[WasteReportResponse],
)
def get_waste_report():

    uow = UnitOfWork()

    with uow:

        service = WasteService(uow)

        return service.get_waste_report()


# =========================
# PRODUCT WASTE HISTORY
# =========================

@router.get(
    "/product/{product_id}",
)
def get_product_waste(
    product_id: int,
):

    uow = UnitOfWork()

    with uow:

        service = WasteService(uow)

        return service.get_product_waste(
            product_id
        )


# =========================
# GET WASTE BY ID
# =========================

@router.get(
    "/{waste_id}",
    response_model=WasteDetailResponse,
)
def get_waste(
    waste_id: int,
):

    uow = UnitOfWork()

    with uow:

        service = WasteService(uow)

        return service.get_waste_by_id(
            waste_id
        )