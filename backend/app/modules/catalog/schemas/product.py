# app/modules/catalog/schemas/product.py
import re
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.common.enums import ProductStatus
from app.modules.catalog.schemas.attribute import (
    ProductAttributeRead,
    ProductVariantAttributeRead,
)
from app.modules.catalog.schemas.brand import BrandRead
from app.modules.catalog.schemas.category import CategoryRead
from app.modules.catalog.schemas.image import GetImage
from app.modules.catalog.schemas.inventory import InventoryRead
from app.modules.catalog.schemas.tag import TagRead


# =========================================================
# Create a Draft Product
# =========================================================
class DraftProductCreate(BaseModel):
    name: str
    description: str = ""

    price: int = Field(..., gt=0)
    discount_price: int | None = Field(None, ge=0)
    cost_price: int | None = Field(None, ge=0)
    tax_rate: int = Field(default=0, ge=0)

    # status: ProductStatus = Field(default=ProductStatus.DRAFT)
    # is_featured: bool = Field(default=False)
    is_digital: bool = Field(default=False)

    weight: Decimal | None = Field(None, ge=0, max_digits=10, decimal_places=3)

    meta_title: str | None = Field(None, max_length=255)
    meta_description: str | None = Field(None, max_length=500)
    gtin: str | None = Field(None, max_length=20)

    @model_validator(mode="after")
    def check_discount(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price must be less than price")
        return self


# =========================================================
# Get Product Data for Admin
# =========================================================
class ProductAdminRead(BaseModel):
    id: int
    name: str
    slug: str | None
    sku: str
    description: str | None

    price: int
    discount_price: int | None
    cost_price: int | None

    tax_rate: int
    discount_percent: float

    final_price: int

    total_available_quantity: int
    is_in_stock: bool

    currency_code: str
    status: ProductStatus

    is_featured: bool
    is_digital: bool

    weight: Decimal | None

    meta_title: str | None
    meta_description: str | None
    gtin: str | None

    created_at: datetime
    updated_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None

    brand: BrandRead | None

    categories: list[CategoryRead] | None

    tags: list[TagRead] | None

    images: list[GetImage] | None

    product_attributes: list[ProductAttributeRead] | None = []

    variant_attributes: list[ProductVariantAttributeRead] | None = []

    inventory: list[InventoryRead] | None = []

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# Get Product Data for steps
# =========================================================
class ProductSimpleRead(BaseModel):
    id: int
    name: str
    slug: str | None
    sku: str
    description: str | None

    price: int
    discount_price: int | None
    cost_price: int | None

    tax_rate: int
    final_price: int
    discount_percent: float

    currency_code: str
    status: ProductStatus

    is_featured: bool
    is_digital: bool

    weight: Decimal | None

    meta_title: str | None
    meta_description: str | None
    gtin: str | None

    created_at: datetime
    updated_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# Update Product Data
# =========================================================
class ProductAdminUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    sku: str | None = None
    description: str | None = None

    price: int | None = None
    discount_price: int | None = None
    cost_price: int | None = None

    tax_rate: int | None = None

    currency_code: str | None = None
    status: ProductStatus | None = ProductStatus.ARCHIVED

    is_featured: bool | None = None
    is_digital: bool | None = None

    weight: Decimal | None = None
    width: Decimal | None = None
    height: Decimal | None = None
    depth: Decimal | None = None

    meta_title: str | None = None
    meta_description: str | None = None
    gtin: str | None = None

    published_at: datetime | None = None
    deleted_at: datetime | None = None

    @field_validator("price", "discount_price", "cost_price", "tax_rate")
    @classmethod
    def non_negative_ints(cls, v):
        if v is not None and v < 0:
            raise ValueError("must be >= 0")
        return v

    @field_validator("tax_rate")
    @classmethod
    def tax_rate_range(cls, v):
        if v is not None and not (500 <= v <= 10000):
            raise ValueError("tax_rate must be between 500 and 10000")
        return v

    @field_validator("weight", "width", "height", "depth")
    @classmethod
    def positive_decimals(cls, v):
        if v is not None and v <= 0:
            raise ValueError("must be > 0")
        return v

    @field_validator("currency_code")
    @classmethod
    def currency_code_format(cls, v):
        if v is not None and not re.fullmatch(r"[A-Z]{3}", v):
            raise ValueError("invalid currency code")
        return v

    @model_validator(mode="after")
    def cross_field_checks(self):
        if self.price is not None and self.discount_price is not None:
            if self.discount_price > self.price:
                raise ValueError("discount_price cannot exceed price")
        if self.published_at and self.deleted_at:
            if self.published_at > self.deleted_at:
                raise ValueError("published_at must be <= deleted_at")
        if self.is_digital:
            if any([self.weight, self.width, self.height, self.depth]):
                raise ValueError("digital product should not have dimensions")
        return self
