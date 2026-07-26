import math

from app.core.unit_of_work import UnitOfWork

from app.core.exceptions import (
    ProductNotFoundException,
    CategoryNotFoundException
)


class ProductService:


    # =========================
    # PRIVATE HELPERS
    # =========================

    def _validate_category(
        self,
        uow,
        category_id: int
    ):

        category = uow.categories.get_category_by_id(
            category_id
        )

        if not category:
            raise CategoryNotFoundException()

        return category



    def _calculate_pages(
        self,
        total: int,
        limit: int
    ):

        if total == 0:
            return 0

        return math.ceil(
            total / limit
        )



    # =========================
    # CREATE PRODUCT
    # =========================

    def create_product(
        self,
        product_data
    ):

        with UnitOfWork() as uow:

            self._validate_category(
                uow,
                product_data.category_id
            )


            return uow.products.create_product(
                product_data.name,
                product_data.description,
                product_data.price,
                product_data.stock,
                product_data.is_active,
                product_data.category_id
            )



    # =========================
    # GET PRODUCTS PAGINATED
    # =========================

    def get_products_paginated(
        self,
        page: int,
        limit: int,
        category_id=None,
        search=None,
        sort=None
    ):

        with UnitOfWork() as uow:

            products = uow.products.get_products_paginated(
                page,
                limit,
                category_id,
                search,
                sort
            )


            total = uow.products.count_products(
                category_id,
                search
            )


            return {
                "data": products,

                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": self._calculate_pages(
                        total,
                        limit
                    )
                }
            }



    # =========================
    # GET PRODUCT BY ID
    # =========================

    def get_product_by_id(
        self,
        product_id: int
    ):

        with UnitOfWork() as uow:

            product = uow.products.get_product_by_id(
                product_id
            )


            if not product:
                raise ProductNotFoundException()


            return product



    # =========================
    # UPDATE PRODUCT
    # =========================

    def update_product(
        self,
        product_id: int,
        product_data
    ):

        with UnitOfWork() as uow:


            if product_data.category_id is not None:

                self._validate_category(
                    uow,
                    product_data.category_id
                )



            product = uow.products.update_product(
                product_id,
                product_data.name,
                product_data.description,
                product_data.price,
                product_data.stock,
                product_data.is_active,
                product_data.category_id
            )


            if not product:
                raise ProductNotFoundException()


            return product



    # =========================
    # DELETE PRODUCT
    # =========================

    def delete_product(
        self,
        product_id: int
    ):

        with UnitOfWork() as uow:

            deleted_product = uow.products.delete_product(
                product_id
            )


            if not deleted_product:
                raise ProductNotFoundException()


            # Return deleted resource id
            # for REST response consistency
            return {
                "id": deleted_product["id"]
            }