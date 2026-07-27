from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

# =====================================================
# REQUEST SCHEMAS
# =====================================================


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)

    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):

    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderUpdate(BaseModel):

    items: list[OrderItemCreate] = Field(..., min_length=1)


# =====================================================
# RESPONSE SCHEMAS
# =====================================================


class OrderItemResponse(BaseModel):

    product_id: int

    quantity: int

    price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):

    order_id: int

    user_id: int

    total_price: Decimal

    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderSummary(BaseModel):

    id: int

    user_id: int

    total_price: Decimal

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderDetail(BaseModel):

    id: int

    user_id: int

    total_price: Decimal

    created_at: datetime

    items: list[OrderItemResponse]

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

    data: list[OrderSummary]

    model_config = ConfigDict(from_attributes=True)
