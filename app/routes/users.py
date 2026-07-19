from fastapi import APIRouter, Depends

from app.schemas.user import (
    UserProfileResponse,
    UserListResponse,
    UserUpdate,
    ChangePasswordRequest,
    UpdateUserRoleRequest,
    UserStatusResponse,
)

from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_user_service():
    return UserService()


# =========================
# GET USER BY ID
# =========================

@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.get_user_by_id(
        user_id
    )


# =========================
# GET ALL USERS
# =========================

@router.get("/", response_model=UserListResponse)
def get_users(
    limit: int = 20,
    offset: int = 0,
    service: UserService = Depends(get_user_service)
):
    return service.get_users(
        limit,
        offset
    )


# =========================
# UPDATE PROFILE
# =========================

@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return service.update_profile(
        user_id,
        data
    )


# =========================
# CHANGE PASSWORD
# =========================

@router.patch("/{user_id}/password")
def change_password(
    user_id: int,
    data: ChangePasswordRequest,
    service: UserService = Depends(get_user_service)
):
    return service.change_password(
        user_id,
        data.old_password,
        data.new_password
    )


# =========================
# UPDATE ROLE
# =========================

@router.patch("/{user_id}/role")
def update_role(
    user_id: int,
    data: UpdateUserRoleRequest,
    service: UserService = Depends(get_user_service)
):
    return service.update_role(
        user_id,
        data.role
    )


# =========================
# ACTIVATE USER
# =========================

@router.patch("/{user_id}/activate")
def activate_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.activate_user(
        user_id
    )


# =========================
# DEACTIVATE USER
# =========================

@router.patch("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.deactivate_user(
        user_id
    )


# =========================
# DELETE USER
# =========================

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.delete_user(
        user_id
    )


# =========================
# RESTORE USER
# =========================

@router.patch("/{user_id}/restore")
def restore_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.restore_user(
        user_id
    )