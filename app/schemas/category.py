from datetime import datetime

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

    description: str | None = None



# =========================
# UPDATE CATEGORY
# =========================

class CategoryUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: str | None = None



# =========================
# RESPONSE
# =========================

class CategoryResponse(BaseModel):

    id: int
    name: str
    description: str | None
    created_at: datetime


    class Config:
        from_attributes = True