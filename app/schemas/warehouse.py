from datetime import datetime

from pydantic import BaseModel


# =========================
# CREATE WAREHOUSE
# =========================

class WarehouseCreate(BaseModel):

    name: str
    location: str | None = None


# =========================
# RESPONSE
# =========================

class WarehouseResponse(BaseModel):

    id: int
    name: str
    location: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# =========================
# ADD PRODUCT
# =========================

class WarehouseInventoryCreate(BaseModel):

    product_id: int
    quantity: int


# =========================
# INVENTORY RESPONSE
# =========================

class WarehouseInventoryResponse(BaseModel):

    id: int
    warehouse_id: int
    product_id: int
    product_name: str
    quantity: int