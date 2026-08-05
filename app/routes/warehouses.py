from fastapi import APIRouter, Depends

from app.core.unit_of_work import UnitOfWork
from app.services.warehouse_service import WarehouseService
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseResponse,
    WarehouseInventoryCreate,
)


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"],
)


def get_service():

    uow = UnitOfWork()

    with uow:
        return WarehouseService(uow)



# =========================
# CREATE
# =========================

@router.post(
    "",
    response_model=WarehouseResponse,
    status_code=201,
)
def create_warehouse(
    payload: WarehouseCreate,
):

    with UnitOfWork() as uow:

        service = WarehouseService(uow)

        return service.create_warehouse(
            payload.model_dump()
        )



# =========================
# GET ALL
# =========================

@router.get("")
def get_warehouses():

    with UnitOfWork() as uow:

        service = WarehouseService(uow)

        return service.get_all_warehouses()



# =========================
# GET BY ID
# =========================

@router.get("/{warehouse_id}")
def get_warehouse(
    warehouse_id: int,
):

    with UnitOfWork() as uow:

        service = WarehouseService(uow)

        return service.get_warehouse_by_id(
            warehouse_id
        )



# =========================
# ADD PRODUCT
# =========================

@router.post("/{warehouse_id}/products")
def add_product(
    warehouse_id: int,
    payload: WarehouseInventoryCreate,
):

    with UnitOfWork() as uow:

        service = WarehouseService(uow)

        return service.add_product(
            warehouse_id,
            payload.model_dump(),
        )



# =========================
# INVENTORY
# =========================

@router.get("/{warehouse_id}/inventory")
def get_inventory(
    warehouse_id: int,
):

    with UnitOfWork() as uow:

        service = WarehouseService(uow)

        return service.get_inventory(
            warehouse_id
        )