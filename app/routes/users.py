from fastapi import APIRouter, Depends, status

from app.schemas.user import (
    ChangePasswordRequest,
    UpdateUserRoleRequest,
    UserListResponse,
    UserProfileResponse,
    UserStatusResponse,
    UserUpdate,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service() -> UserService:
    """
    Returns an instance of UserService.
    """
    return UserService()


# ==================================================
# GET USER BY ID
# ==================================================


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.get_user_by_id(
        user_id,
    )


# ==================================================
# GET USERS PAGINATED
# ==================================================


@router.get(
    "/",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
)
def get_users(
    limit: int = 20,
    offset: int = 0,
    service: UserService = Depends(get_user_service),
) -> UserListResponse:

    return service.get_users(
        limit,
        offset,
    )


# ==================================================
# UPDATE PROFILE
# ==================================================


@router.put(
    "/{user_id}",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.update_profile(
        user_id,
        data,
    )


# ==================================================
# CHANGE PASSWORD
# ==================================================


@router.patch(
    "/{user_id}/password",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def change_password(
    user_id: int,
    data: ChangePasswordRequest,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.change_password(
        user_id,
        data.old_password,
        data.new_password,
    )


# ==================================================
# UPDATE ROLE
# ==================================================


@router.patch(
    "/{user_id}/role",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def update_role(
    user_id: int,
    data: UpdateUserRoleRequest,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.update_role(
        user_id,
        data.role,
    )


# ==================================================
# ACTIVATE USER
# ==================================================


@router.patch(
    "/{user_id}/activate",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def activate_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserStatusResponse:

    return service.activate_user(
        user_id,
    )


# ==================================================
# DEACTIVATE USER
# ==================================================


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def deactivate_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.deactivate_user(
        user_id,
    )


# ==================================================
# DELETE USER (SOFT DELETE)
# ==================================================


@router.delete(
    "/{user_id}",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.delete_user(
        user_id,
    )


# ==================================================
# RESTORE USER
# ==================================================


@router.patch(
    "/{user_id}/restore",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def restore_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserProfileResponse:

    return service.restore_user(
        user_id,
    )
