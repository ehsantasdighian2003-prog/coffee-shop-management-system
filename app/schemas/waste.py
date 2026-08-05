from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_serializer


# =========================
# CREATE WASTE
# =========================

class WasteCreate(BaseModel):

    product_id: int

    warehouse_id: int

    quantity: int = Field(
        gt=0
    )

    reason: str

    cost: Decimal = Decimal("0")


# =========================
# RESPONSE
# =========================

class WasteResponse(BaseModel):

    id: int

    product_id: int

    warehouse_id: int

    quantity: int

    reason: str

    cost: Decimal

    created_by: int | None = None

    created_at: datetime

    updated_at: datetime


    @field_serializer(
        "cost"
    )
    def serialize_cost(
        self,
        value: Decimal,
    ):
        return f"{value:.2f}"


# =========================
# DETAIL RESPONSE
# =========================

class WasteDetailResponse(BaseModel):

    id: int

    product_id: int

    product_name: str

    warehouse_id: int

    warehouse_name: str

    quantity: int

    reason: str

    cost: Decimal

    created_by: int | None = None

    created_at: datetime

    updated_at: datetime


    @field_serializer(
        "cost"
    )
    def serialize_cost(
        self,
        value: Decimal,
    ):
        return f"{value:.2f}"
    
    
# =========================
# WASTE REPORT
# =========================

class WasteReportResponse(BaseModel):

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