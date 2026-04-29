from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str | None = Field(None, max_length=120)
    description: str | None = Field(None, max_length=500)
    is_active: bool = True
    parent_id: int | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    slug: str | None = Field(None, max_length=120)
    description: str | None = Field(None, max_length=500)
    is_active: bool | None = None
    parent_id: int | None = None


class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str | None
    description: str | None
    is_active: bool
    parent_id: int | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
