from app.core.exceptions import CategoryNotFoundException
from app.core.unit_of_work import UnitOfWork

from app.repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self):

        self.repo = CategoryRepository()

    # =========================
    # PRIVATE HELPERS
    # =========================

    def _get_category_or_raise(
        self,
        conn,
        category_id: int
    ):

        category = self.repo.get_category_by_id(
            conn,
            category_id
        )

        if not category:
            raise CategoryNotFoundException()

        return category

    # =========================
    # CREATE CATEGORY
    # =========================

    def create_category(
        self,
        category_data
    ):

        with UnitOfWork() as uow:

            return self.repo.create_category(
                uow.conn,
                category_data.name,
                category_data.description
            )

    # =========================
    # GET ALL CATEGORIES
    # =========================

    def get_all_categories(self):

        with UnitOfWork() as uow:

            return self.repo.get_all_categories(
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

            return self._get_category_or_raise(
                uow.conn,
                category_id
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

            category = self.repo.update_category(
                uow.conn,
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

            deleted_category = self.repo.delete_category(
                uow.conn,
                category_id
            )

            if not deleted_category:
                raise CategoryNotFoundException()

            return {
                "message": "Category deleted successfully.",
                "category_id": deleted_category["id"]
            }