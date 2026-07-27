from app.core.exceptions import CategoryNotFoundException
from app.core.unit_of_work import UnitOfWork


class CategoryService:

    # =========================
    # PRIVATE HELPERS
    # =========================

    def _get_category_or_raise(self, uow, category_id: int):

        category = uow.categories.get_category_by_id(category_id)

        if not category:
            raise CategoryNotFoundException()

        return category

    # =========================
    # CREATE CATEGORY
    # =========================

    def create_category(self, category_data):

        with UnitOfWork() as uow:

            return uow.categories.create_category(
                category_data.name, category_data.description
            )

    # =========================
    # GET ALL CATEGORIES
    # =========================

    def get_all_categories(self):

        with UnitOfWork() as uow:

            return uow.categories.get_all_categories()

    # =========================
    # GET CATEGORY BY ID
    # =========================

    def get_category_by_id(self, category_id: int):

        with UnitOfWork() as uow:

            return self._get_category_or_raise(uow, category_id)

    # =========================
    # UPDATE CATEGORY
    # =========================

    def update_category(self, category_id: int, category_data):

        with UnitOfWork() as uow:

            category = uow.categories.update_category(
                category_id, category_data.name, category_data.description
            )

            if not category:
                raise CategoryNotFoundException()

            return category

    # =========================
    # DELETE CATEGORY
    # =========================

    def delete_category(self, category_id: int):

        with UnitOfWork() as uow:

            deleted_category = uow.categories.delete_category(category_id)

            if not deleted_category:
                raise CategoryNotFoundException()

            return {
                "message": "Category deleted successfully.",
                "category_id": deleted_category["id"],
            }
