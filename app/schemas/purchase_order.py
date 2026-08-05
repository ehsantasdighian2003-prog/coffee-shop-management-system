from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class PurchaseOrderStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class PurchaseOrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    notes: str | None = None
    items: list[PurchaseOrderItemCreate]


class PurchaseOrderUpdate(BaseModel):
    status: PurchaseOrderStatus | None = None
    notes: str | None = None


class PurchaseOrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        from_attributes = True


class PurchaseOrderResponse(BaseModel):
    id: int
    supplier_id: int
    status: PurchaseOrderStatus
    total_amount: Decimal
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    items: list[PurchaseOrderItemResponse] = []

    class Config:
        from_attributes = True