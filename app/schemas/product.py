from pydantic import BaseModel, Field
from typing import Optional, List


# =========================
# CATEGORY SIMPLE RESPONSE
# =========================

class CategorySimple(BaseModel):

    id: int
    name: str


# =========================
# CREATE PRODUCT
# =========================

class ProductCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None

    price: float = Field(
        ...,
        gt=0
    )

    stock: int = Field(
        ...,
        ge=0
    )

    is_active: bool = True

    category_id: int


# =========================
# UPDATE PRODUCT
# =========================

class ProductUpdate(BaseModel):

    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None

    price: Optional[float] = Field(
        None,
        gt=0
    )

    stock: Optional[int] = Field(
        None,
        ge=0
    )

    is_active: Optional[bool] = None

    category_id: Optional[int] = None


# =========================
# PRODUCT RESPONSE
# =========================

class ProductResponse(BaseModel):

    id: int

    name: str

    description: Optional[str] = None

    price: float

    stock: int

    is_active: bool

    category: Optional[CategorySimple] = None


# =========================
# PRODUCT SUMMARY
# =========================

class ProductSummary(BaseModel):

    id: int

    name: str

    price: float

    stock: int

    is_active: bool

    category: Optional[CategorySimple] = None


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

    data: List[ProductResponse]

    meta: PaginationMeta
