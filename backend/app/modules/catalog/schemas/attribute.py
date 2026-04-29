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
    value: str = Field(..., max_length=255)


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
    variant_id: int
    attribute_id: int
    value: str = Field(..., max_length=255)


class ProductVariantAttributeUpdate(BaseModel):
    value: str = Field(..., max_length=255)


class ProductVariantAttributeRead(BaseModel):
    id: int
    variant_id: int
    attribute_id: int
    value: str

    class Config:
        from_attributes = True
