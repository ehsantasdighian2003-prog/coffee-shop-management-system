from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


class InventoryTransactionCreate(BaseModel):
    product_id: int
    transaction_type: TransactionType
    quantity: int

    supplier_id: int | None = None
    order_id: int | None = None

    note: str | None = None


class InventoryTransactionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int
    product_id: int

    transaction_type: TransactionType

    quantity: int

    supplier_id: int | None = None
    order_id: int | None = None

    note: str | None = None

    created_at: datetime


class StockMovementResponse(BaseModel):
    product_id: int
    product_name: str

    total_in: int
    total_out: int

    current_stock: int
    
    
class InventoryTransactionReverse(BaseModel):
    note: str | None = None