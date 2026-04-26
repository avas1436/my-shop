from pydantic import BaseModel, field_validator

from app.common.validators import validate_price


class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    category_id: int

    @field_validator("price")
    @classmethod
    def validate_product_price(cls, value: float) -> float:
        return validate_price(value)


class ProductRead(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: float
    category_id: int

    class Config:
        from_attributes = True
