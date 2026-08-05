from datetime import date, datetime

from pydantic import BaseModel



# =========================
# CREATE BATCH
# =========================

class ProductBatchCreate(BaseModel):

    product_id: int
    warehouse_id: int

    batch_number: str

    quantity: int

    production_date: date | None = None

    expiration_date: date



# =========================
# RESPONSE
# =========================

class ProductBatchResponse(BaseModel):

    id: int

    product_id: int
    warehouse_id: int

    batch_number: str

    quantity: int

    production_date: date | None

    expiration_date: date

    created_at: datetime
    updated_at: datetime



# =========================
# DETAILED RESPONSE
# =========================

class ProductBatchDetailResponse(BaseModel):

    id: int

    product_id: int
    product_name: str

    warehouse_id: int
    warehouse_name: str

    batch_number: str

    quantity: int

    production_date: date | None

    expiration_date: date

    created_at: datetime
    updated_at: datetime