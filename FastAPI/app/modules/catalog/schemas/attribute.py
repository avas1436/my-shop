# app/modules/catalog/schemas/attribute.py
from datetime import datetime

from pydantic import BaseModel, Field


# --------------------------------------------------
# Attribure Schema
# --------------------------------------------------
class AttributeCreate(BaseModel):
    name: str = Field(..., max_length=120)
    slug: str | None = Field(None, max_length=150)


class AttributeUpdate(BaseModel):
    name: str | None = Field(None, max_length=120)
    slug: str | None = Field(None, max_length=150)


class AttributeRead(BaseModel):
    id: int
    name: str
    slug: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# --------------------------------------------------
# Product Attribure Schema
# --------------------------------------------------
class ProductAttributeCreate(BaseModel):
    product_id: int
    attribute_id: int
    value: str = Field(..., max_length=255)


class ProductAttributeUpdate(BaseModel):
    product_id: int
    value: str = Field(..., max_length=255)


class DeleteProductAttribute(BaseModel):
    product_id: int
    product_attribute_id: int


class ProductAttributeRead(BaseModel):
    id: int
    product_id: int
    attribute_id: int
    value: str

    class Config:
        from_attributes = True


# --------------------------------------------------
# Product Variant Attribure Schema
# --------------------------------------------------
class ProductVariantAttributeCreate(BaseModel):
    product_id: int
    variant_id: int
    attribute_id: int
    value: str = Field(..., max_length=255)


class ProductVariantAttributeUpdate(BaseModel):
    product_id: int
    value: str = Field(..., max_length=255)


class DeleteProductVariantAttribute(BaseModel):
    product_id: int
    product_variant_attribute_id: int


class ProductVariantAttributeRead(BaseModel):
    id: int
    variant_id: int
    attribute_id: int
    value: str

    class Config:
        from_attributes = True
