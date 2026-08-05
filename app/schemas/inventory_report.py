from decimal import Decimal

from pydantic import BaseModel, field_serializer


# =========================
# STOCK SUMMARY REPORT
# =========================

class StockSummaryReportResponse(BaseModel):

    product_id: int

    product_name: str

    current_stock: int


# =========================
# INVENTORY MOVEMENT REPORT
# =========================

class InventoryMovementReportResponse(BaseModel):

    product_id: int

    product_name: str

    total_in: int

    total_out: int

    current_stock: int


# =========================
# WASTE COST REPORT
# =========================

class WasteCostReportResponse(BaseModel):

    product_id: int

    product_name: str

    total_quantity: int

    total_cost: Decimal


    @field_serializer(
        "total_cost"
    )
    def serialize_total_cost(
        self,
        value: Decimal,
    ):
        return f"{value:.2f}"


# =========================
# WAREHOUSE STOCK REPORT
# =========================

class WarehouseStockReportResponse(BaseModel):

    warehouse_id: int

    warehouse_name: str

    product_id: int

    product_name: str

    quantity: int


# =========================
# EXPIRING BATCH REPORT
# =========================

class ExpiringBatchReportResponse(BaseModel):

    batch_id: int

    product_id: int

    product_name: str

    warehouse_id: int

    warehouse_name: str

    batch_number: str

    quantity: int

    expiration_date: str