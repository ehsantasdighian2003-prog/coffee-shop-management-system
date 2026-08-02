from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


class InventoryTransactionCreate(BaseModel):
    product_id: int
    transaction_type: TransactionType
    quantity: Decimal
    note: str | None = None


class InventoryTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    transaction_type: TransactionType
    quantity: Decimal
    note: str | None
    created_at: datetime