from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

# =========================
# CATEGORY SIMPLE RESPONSE
# =========================


class CategorySimple(BaseModel):

    id: int

    name: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# CREATE PRODUCT
# =========================


class ProductCreate(BaseModel):

    name: str = Field(..., min_length=2, max_length=100)

    description: str | None = None

    price: Decimal = Field(..., gt=0)

    stock: int = Field(..., ge=0)

    is_active: bool = True

    category_id: int = Field(..., gt=0)


# =========================
# UPDATE PRODUCT
# =========================


class ProductUpdate(BaseModel):

    name: str | None = Field(None, min_length=2, max_length=100)

    description: str | None = None

    price: Decimal | None = Field(None, gt=0)

    stock: int | None = Field(None, ge=0)

    is_active: bool | None = None

    category_id: int | None = Field(None, gt=0)


# =========================
# PRODUCT RESPONSE
# =========================


class ProductResponse(BaseModel):

    id: int

    name: str

    description: str | None = None

    price: Decimal

    stock: int

    is_active: bool

    # optional because repository may return nested category only
    category_id: int | None = None

    category: CategorySimple | None = None

    @field_serializer("price")
    def serialize_price(self, value: Decimal):
        return float(value)

    model_config = ConfigDict(from_attributes=True)


# =========================
# PRODUCT SUMMARY
# =========================


class ProductSummary(BaseModel):

    id: int

    name: str

    price: Decimal

    stock: int

    is_active: bool

    category_id: int | None = None

    category: CategorySimple | None = None

    @field_serializer("price")
    def serialize_price(self, value: Decimal):
        return float(value)

    model_config = ConfigDict(from_attributes=True)


# =========================
# PAGINATION META
# =========================


class PaginationMeta(BaseModel):

    page: int

    limit: int

    total: int

    pages: int


# =========================
# PRODUCT PAGINATED RESPONSE
# =========================


class ProductListResponse(BaseModel):

    data: list[ProductResponse]

    meta: PaginationMeta
