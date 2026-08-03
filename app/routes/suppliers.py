from fastapi import APIRouter, Depends, Query, status

from app.core.security import admin_required
from app.schemas.supplier import (
    SupplierCreate,
    SupplierListResponse,
    SupplierResponse,
    SupplierUpdate,
)
from app.services.supplier_service import SupplierService

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

supplier_service = SupplierService()


# =========================
# CREATE SUPPLIER
# =========================

@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)],
)
def create_supplier(supplier: SupplierCreate):

    return supplier_service.create_supplier(supplier)


# =========================
# GET SUPPLIERS
# =========================

@router.get("/", response_model=SupplierListResponse)
def get_suppliers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
):

    return supplier_service.get_suppliers_paginated(
        page,
        limit,
        search,
    )


# =========================
# GET SUPPLIER BY ID
# =========================

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier_by_id(supplier_id: int):

    return supplier_service.get_supplier_by_id(supplier_id)


# =========================
# UPDATE SUPPLIER
# =========================

@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse,
    dependencies=[Depends(admin_required)],
)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
):

    return supplier_service.update_supplier(
        supplier_id,
        supplier,
    )


# =========================
# DELETE SUPPLIER
# =========================

@router.delete(
    "/{supplier_id}",
    dependencies=[Depends(admin_required)],
)
def delete_supplier(supplier_id: int):

    return supplier_service.delete_supplier(supplier_id)


# =========================
# RESTORE SUPPLIER
# =========================

@router.patch(
    "/{supplier_id}/restore",
    response_model=SupplierResponse,
    dependencies=[Depends(admin_required)],
)
def restore_supplier(supplier_id: int):

    return supplier_service.restore_supplier(supplier_id)


# =========================
# ACTIVATE SUPPLIER
# =========================

@router.patch(
    "/{supplier_id}/activate",
    response_model=SupplierResponse,
    dependencies=[Depends(admin_required)],
)
def activate_supplier(supplier_id: int):

    return supplier_service.activate_supplier(supplier_id)


# =========================
# DEACTIVATE SUPPLIER
# =========================

@router.patch(
    "/{supplier_id}/deactivate",
    response_model=SupplierResponse,
    dependencies=[Depends(admin_required)],
)
def deactivate_supplier(supplier_id: int):

    return supplier_service.deactivate_supplier(supplier_id)