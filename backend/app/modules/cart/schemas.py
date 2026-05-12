# app/modules/cart/schemas.py
from __future__ import annotations

from pydantic import BaseModel, Field

from app.common.enums import CartStatus


class CartItemIn(BaseModel):
    variant_id: int
    qty: int = Field(gt=0)


class CartSyncRequest(BaseModel):
    items: list[CartItemIn] = Field(min_length=1)


class CartItemOut(BaseModel):
    variant_id: int
    qty: int


class CartOut(BaseModel):
    user_id: int
    status: CartStatus
    total_amount: int
    discount: int
    items: list[CartItemOut]
