from app.core.exceptions import SupplierNotFoundException
from app.core.unit_of_work import UnitOfWork


class SupplierService:

    # =========================
    # CREATE SUPPLIER
    # =========================

    def create_supplier(self, supplier_data):

        with UnitOfWork() as uow:

            return uow.suppliers.create_supplier(
                supplier_data.name,
                supplier_data.phone,
                supplier_data.email,
                supplier_data.address,
            )


    # =========================
    # GET SUPPLIER BY ID
    # =========================

    def get_supplier_by_id(self, supplier_id: int):

        with UnitOfWork() as uow:

            supplier = uow.suppliers.get_supplier_by_id(
                supplier_id
            )

            if not supplier:
                raise SupplierNotFoundException()

            return supplier


    # =========================
    # GET SUPPLIERS PAGINATED
    # =========================

    def get_suppliers_paginated(
        self,
        page: int,
        limit: int,
        search=None,
    ):

        with UnitOfWork() as uow:

            suppliers = uow.suppliers.get_suppliers_paginated(
                page,
                limit,
                search,
            )

            total = uow.suppliers.count_suppliers(
                search
            )

            pages = (
                (total + limit - 1) // limit
                if total > 0
                else 0
            )

            return {
                "data": suppliers,
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": pages,
                },
            }


    # =========================
    # UPDATE SUPPLIER
    # =========================

    def update_supplier(
        self,
        supplier_id: int,
        supplier_data,
    ):

        with UnitOfWork() as uow:

            supplier = uow.suppliers.update_supplier(
                supplier_id,
                supplier_data.name,
                supplier_data.phone,
                supplier_data.email,
                supplier_data.address,
            )

            if not supplier:
                raise SupplierNotFoundException()

            return supplier


    # =========================
    # DELETE SUPPLIER
    # =========================

    def delete_supplier(
        self,
        supplier_id: int,
    ):

        with UnitOfWork() as uow:

            supplier = uow.suppliers.delete_supplier(
                supplier_id
            )

            if not supplier:
                raise SupplierNotFoundException()

            return {
                "id": supplier["id"]
            }


    # =========================
    # RESTORE SUPPLIER
    # =========================

    def restore_supplier(
        self,
        supplier_id: int,
    ):

        with UnitOfWork() as uow:

            supplier = uow.suppliers.restore_supplier(
                supplier_id
            )

            if not supplier:
                raise SupplierNotFoundException()

            return supplier
        
        
    # =========================
    # ACTIVATE SUPPLIER
    # =========================

    def activate_supplier(
        self,
        supplier_id: int,
    ):

        with UnitOfWork() as uow:

            supplier = uow.suppliers.activate_supplier(
                supplier_id
            )

            if not supplier:
                raise SupplierNotFoundException()

            return supplier


    # =========================
    # DEACTIVATE SUPPLIER
    # =========================

    def deactivate_supplier(
        self,
        supplier_id: int,
    ):

        with UnitOfWork() as uow:

            supplier = uow.suppliers.deactivate_supplier(
                supplier_id
            )

            if not supplier:
                raise SupplierNotFoundException()

            return supplier