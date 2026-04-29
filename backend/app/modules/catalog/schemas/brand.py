# app/modules/catalog/shcemas/brand.py
from datetime import datetime

from pydantic import BaseModel, Field


class BrandCreate(BaseModel):
    name: str = Field(..., max_length=150)
    slug: str | None = Field(None, max_length=180)


class BrandUpdate(BaseModel):
    name: str | None = Field(None, max_length=150)
    slug: str | None = Field(None, max_length=180)


class BrandRead(BaseModel):
    id: int
    name: str
    slug: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
