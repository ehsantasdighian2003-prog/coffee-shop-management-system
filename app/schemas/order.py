from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


# =====================================================
# REQUEST SCHEMAS
# =====================================================

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    items: List[OrderItemCreate]


# =====================================================
# RESPONSE SCHEMAS
# =====================================================

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    total_price: float
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderSummary(BaseModel):
    id: int
    user_id: int
    total_price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderDetail(BaseModel):
    id: int
    user_id: int
    total_price: float
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# PAGINATION
# =====================================================

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    pages: int


class PaginatedOrdersResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    data: List[OrderSummary]

    model_config = ConfigDict(from_attributes=True)