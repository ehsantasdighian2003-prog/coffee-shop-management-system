from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# =========================
# CREATE CATEGORY
# =========================

class CategoryCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None


# =========================
# UPDATE CATEGORY
# =========================

class CategoryUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None


# =========================
# RESPONSE
# =========================

class CategoryResponse(BaseModel):

    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }