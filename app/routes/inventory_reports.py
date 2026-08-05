from fastapi import APIRouter, Query

from app.core.unit_of_work import UnitOfWork
from app.services.inventory_report_service import (
    InventoryReportService,
)


router = APIRouter(
    prefix="/inventory-reports",
    tags=["Inventory Reports"],
)


# =========================
# STOCK SUMMARY
# =========================

@router.get(
    "/stock-summary",
)
def stock_summary():

    uow = UnitOfWork()

    with uow:

        service = InventoryReportService(
            uow
        )

        return service.get_stock_summary()



# =========================
# INVENTORY MOVEMENTS
# =========================

@router.get(
    "/movements",
)
def inventory_movements():

    uow = UnitOfWork()

    with uow:

        service = InventoryReportService(
            uow
        )

        return service.get_inventory_movements()



# =========================
# WASTE COST
# =========================

@router.get(
    "/waste-cost",
)
def waste_cost():

    uow = UnitOfWork()

    with uow:

        service = InventoryReportService(
            uow
        )

        return service.get_waste_cost_report()



# =========================
# WAREHOUSE STOCK
# =========================

@router.get(
    "/warehouse-stock",
)
def warehouse_stock():

    uow = UnitOfWork()

    with uow:

        service = InventoryReportService(
            uow
        )

        return service.get_warehouse_stock_report()



# =========================
# EXPIRING BATCHES
# =========================

@router.get(
    "/expiring-batches",
)
def expiring_batches(
    days: int = Query(
        30,
        ge=1,
    ),
):

    uow = UnitOfWork()

    with uow:

        service = InventoryReportService(
            uow
        )

        return service.get_expiring_batches(
            days
        )