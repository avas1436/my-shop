import re
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from app.common.enums import ProductStatus


# =========================================================
# Create a Draft Product
# =========================================================
class DraftProductCreate(BaseModel):
    name: str
    slug: str | None = None
    description: str = ""

    # قیمت گذاری
    price: int = Field(..., gt=0)
    discount_price: int | None = Field(None, ge=0)
    cost_price: int | None = Field(None, ge=0)
    tax_rate: int = Field(..., gt=0)

    # وضعیت محصول
    status: ProductStatus = Field(default=ProductStatus.DRAFT)
    is_featured: bool = Field(default=False)
    is_digital: bool = Field(default=False)

    # ابعاد و وزن
    weight: Decimal | None = Field(None, ge=0, max_digits=10, decimal_places=3)

    # متادیتا
    meta_title: str | None = Field(None, max_length=255)
    meta_description: str | None = Field(None, max_length=500)

    # بارکد
    gtin: str | None = Field(None, max_length=20)

    @model_validator(mode="after")
    def check_discount(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price must be less than price")

    @model_validator(mode="after")
    def auto_generate_slug(self):

        if not self.slug:
            self.slug = self._generate_slug(self.name)

        return self

    @staticmethod
    def _generate_slug(text: str) -> str:
        text = text.strip()

        text = text.lower()

        allowed_pattern = r"[^0-9a-zA-Zآ-یءئؤچژگپ\s_-]"

        text = re.sub(allowed_pattern, "", text)

        text = re.sub(r"\s+", "-", text)

        text = re.sub(r"-{2,}", "-", text)

        return text.strip("-")


# =========================================================
# Get Product Data for Admin
# =========================================================
class ProductAdminRead(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: float
    category_id: int

    class Config:
        from_attributes = True
