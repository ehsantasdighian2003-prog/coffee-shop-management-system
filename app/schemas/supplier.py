from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SupplierBase(BaseModel):

    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):

    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class SupplierResponse(SupplierBase):

    id: int

    is_active: bool
    is_deleted: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
    
    
class PaginationMeta(BaseModel):

    page: int
    limit: int
    total: int
    pages: int


class SupplierListResponse(BaseModel):

    data: list[SupplierResponse]
    meta: PaginationMeta