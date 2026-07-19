import math

from app.core.unit_of_work import UnitOfWork

from app.core.exceptions import (
    ProductNotFoundException,
    CategoryNotFoundException
)

from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository


class ProductService:

    def __init__(self):

        self.repo = ProductRepository()
        self.category_repo = CategoryRepository()


    # =========================
    # PRIVATE HELPERS
    # =========================

    def _validate_category(
        self,
        conn,
        category_id: int
    ):

        category = self.category_repo.get_category_by_id(
            conn,
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
                uow.conn,
                product_data.category_id
            )

            return self.repo.create_product(
                uow.conn,
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

            products = self.repo.get_products_paginated(
                uow.conn,
                page,
                limit,
                category_id,
                search,
                sort
            )

            total = self.repo.count_products(
                uow.conn,
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

            product = self.repo.get_product_by_id(
                uow.conn,
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
                    uow.conn,
                    product_data.category_id
                )


            product = self.repo.update_product(
                uow.conn,
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

            deleted_product = self.repo.delete_product(
                uow.conn,
                product_id
            )


            if not deleted_product:
                raise ProductNotFoundException()


            return {
                "message": "Product deleted successfully.",
                "product_id": deleted_product["id"]
            }