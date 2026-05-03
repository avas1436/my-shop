# app/modules/catalog/schemas/variant.py
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProductVariantBase(BaseModel):
    price: int | None = Field(default=None, ge=0)
    is_active: bool = True


class ProductVariantCreate(ProductVariantBase):
    product_id: int


class ProductVariantUpdate(BaseModel):
    sku: str | None = Field(default=None, max_length=100)
    price: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductVariantRead(ProductVariantBase):
    id: int
    sku: str
    product_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)
