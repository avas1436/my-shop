from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from app.common.enums import ProductStatus

# =========================================================
# Create a Draft Product
# =========================================================
# schemas/product.py


class DraftProductCreate(BaseModel):
    name: str
    description: str = ""

    price: int = Field(..., gt=0)
    discount_price: int | None = Field(None, ge=0)
    cost_price: int | None = Field(None, ge=0)
    tax_rate: int = Field(default=0, ge=0)

    status: ProductStatus = Field(default=ProductStatus.DRAFT)
    is_featured: bool = Field(default=False)
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
    slug: str
    description: str
    price: float
    category_id: int

    class Config:
        from_attributes = True
