from fastapi import APIRouter, Depends, Query, status

from app.core.security import admin_required
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


product_service = ProductService()


# =========================
# CREATE PRODUCT
# =========================


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)],
)
def create_product(product: ProductCreate):

    return product_service.create_product(product)


# =========================
# GET PRODUCTS
# PAGINATION + FILTER + SEARCH + SORT
# =========================


@router.get("/", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: int | None = Query(None),
    search: str | None = Query(None),
    sort: str | None = Query(None),
):

    return product_service.get_products_paginated(
        page, limit, category_id, search, sort
    )


# =========================
# GET PRODUCT BY ID
# =========================


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int):

    return product_service.get_product_by_id(product_id)


# =========================
# UPDATE PRODUCT
# =========================


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(admin_required)],
)
def update_product(product_id: int, product: ProductUpdate):

    return product_service.update_product(product_id, product)


# =========================
# DELETE PRODUCT
# =========================


@router.delete("/{product_id}", dependencies=[Depends(admin_required)])
def delete_product(product_id: int):

    return product_service.delete_product(product_id)
