from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from app.services.category_service import CategoryService
from app.core.security import admin_required


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


category_service = CategoryService()


# =====================================================
# CREATE CATEGORY (ADMIN ONLY)
# =====================================================

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_required)]
)
def create_category(
    category: CategoryCreate
):

    return category_service.create_category(
        category
    )



# =====================================================
# GET ALL CATEGORIES
# =====================================================

@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def get_all_categories():

    return category_service.get_all_categories()



# =====================================================
# GET CATEGORY BY ID
# =====================================================

@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category_by_id(
    category_id: int
):

    return category_service.get_category_by_id(
        category_id
    )



# =====================================================
# UPDATE CATEGORY (ADMIN ONLY)
# =====================================================

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    dependencies=[Depends(admin_required)]
)
def update_category(
    category_id: int,
    category: CategoryUpdate
):

    return category_service.update_category(
        category_id,
        category
    )



# =====================================================
# DELETE CATEGORY (ADMIN ONLY)
# =====================================================

@router.delete(
    "/{category_id}",
    dependencies=[Depends(admin_required)]
)
def delete_category(
    category_id: int
):

    return category_service.delete_category(
        category_id
    )