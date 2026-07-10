from app.core.exceptions import CategoryNotFoundException
from app.core.unit_of_work import UnitOfWork

from app.repositories.category_repository import CategoryRepository


class CategoryService:

    # =========================
    # CREATE CATEGORY
    # =========================
    def create_category(self, category_data):

        with UnitOfWork() as uow:

            return CategoryRepository.create_category(
                uow.conn,
                category_data.name,
                category_data.description
            )

    # =========================
    # GET ALL CATEGORIES
    # =========================
    def get_all_categories(self):

        with UnitOfWork() as uow:

            return CategoryRepository.get_all_categories(
                uow.conn
            )

    # =========================
    # GET CATEGORY BY ID
    # =========================
    def get_category_by_id(
        self,
        category_id: int
    ):

        with UnitOfWork() as uow:

            category = CategoryRepository.get_category_by_id(
                uow.conn,
                category_id
            )

            if not category:
                raise CategoryNotFoundException()

            return category

    # =========================
    # UPDATE CATEGORY
    # =========================
    def update_category(
        self,
        category_id: int,
        category_data
    ):

        with UnitOfWork() as uow:

            category = CategoryRepository.update_category(
                uow.connection,
                category_id,
                category_data.name,
                category_data.description
            )

            if not category:
                raise CategoryNotFoundException()

            return category

    # =========================
    # DELETE CATEGORY
    # =========================
    def delete_category(
        self,
        category_id: int
    ):

        with UnitOfWork() as uow:

            category = CategoryRepository.delete_category(
                uow.conn,
                category_id
            )

            if not category:
                raise CategoryNotFoundException()

            return {
                "message": "Category deleted successfully."
            }