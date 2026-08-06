from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class MembershipLevel(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    VIP = "VIP"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class CustomerBase(BaseModel):
    full_name: str
    phone: str
    email: EmailStr | None = None
    birthday: date | None = None
    address: str | None = None
    gender: Gender | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    birthday: date | None = None
    address: str | None = None
    gender: Gender | None = None


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    status: CustomerStatus

    loyalty_points: int
    membership_level: MembershipLevel

    is_active: bool
    is_deleted: bool

    created_at: datetime
    updated_at: datetime