from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# =========================
# Base User Schema
# =========================

class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None


# =========================
# Create User
# =========================

class UserCreate(UserBase):
    password: str


# =========================
# Update User
# =========================

class UserUpdate(UserBase):
    pass


# =========================
# Update Role Request
# =========================

class UpdateUserRoleRequest(BaseModel):
    role: Literal["admin", "user"]


# =========================
# Change Password
# =========================

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# =========================
# User Profile Response
# =========================

class UserProfileResponse(BaseModel):
    id: int
    username: str

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None

    role: str
    is_active: bool

    created_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# User List Response
# =========================

class UserListResponse(BaseModel):
    users: List[UserProfileResponse]
    total: int
    page: int
    limit: int


# =========================
# Generic Status Response
# =========================

class UserStatusResponse(BaseModel):
    message: str