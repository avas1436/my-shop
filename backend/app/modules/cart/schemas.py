# app/modules/cart/schemas.py
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import CartStatus, ProductStatus


class CartItemIn(BaseModel):
    variant_id: int
    qty: int = Field(gt=0)


class CartItemOut(BaseModel):
    variant_id: int
    qty: int
    name: str

    price: int
    discount_price: int | None

    tax_rate: int
    final_price: int
    price_with_tax: int
    discount_percent: float

    currency_code: str
    status: ProductStatus

    model_config = ConfigDict(from_attributes=True)


class CartSyncRequest(BaseModel):
    items: list[CartItemIn] = Field(min_length=1)


class CartOut(BaseModel):
    user_id: int
    status: CartStatus
    total_amount: int
    discount: int
    items: list[CartItemOut]
