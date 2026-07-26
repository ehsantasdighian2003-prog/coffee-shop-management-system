from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


# ==================================================
# BASE USER SCHEMA
# ==================================================

class UserBase(BaseModel):
    """
    Common user profile fields.
    """

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    profile_image: str | None = None



# ==================================================
# CREATE USER
# ==================================================

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """

    username: str
    password: str

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    profile_image: str | None = None



# ==================================================
# UPDATE USER PROFILE
# ==================================================

class UserUpdate(UserBase):
    """
    Schema for updating user profile.
    Username cannot be changed here.
    """

    pass



# ==================================================
# UPDATE USER ROLE
# ==================================================

class UpdateUserRoleRequest(BaseModel):
    role: Literal["admin", "user"]



# ==================================================
# CHANGE PASSWORD
# ==================================================

class ChangePasswordRequest(BaseModel):

    old_password: str
    new_password: str



# ==================================================
# USER PROFILE RESPONSE
# ==================================================

class UserProfileResponse(BaseModel):

    id: int

    username: str

    first_name: str | None = None
    last_name: str | None = None

    email: EmailStr | None = None

    phone_number: str | None = None
    profile_image: str | None = None

    role: str

    is_active: bool

    created_at: datetime

    deleted_at: datetime | None = None


    model_config = ConfigDict(
        from_attributes=True
    )



# ==================================================
# PAGINATION METADATA
# ==================================================

class PaginationMeta(BaseModel):

    page: int

    limit: int

    total: int

    pages: int



# ==================================================
# USER LIST RESPONSE
# ==================================================

class UserListResponse(BaseModel):

    data: list[UserProfileResponse]

    meta: PaginationMeta



# ==================================================
# USER STATUS RESPONSE
# ==================================================

class UserStatusResponse(BaseModel):

    message: str