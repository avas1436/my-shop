# app/modules/cart/repository.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_loader_criteria

from app.common.enums import CartStatus
from app.modules.cart.models import Cart, CartItem
from app.modules.catalog.models.image import ProductImage
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.variant import ProductVariant


class CartRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active_cart(self, user_id: int) -> Cart | None:
        stmt = (
            select(Cart)
            .where(
                Cart.user_id == user_id,
                Cart.status == CartStatus.ACTIVE,
            )
            .options(
                # Cart -> items (CartItem)
                selectinload(Cart.items)
                # CartItem -> variant (ProductVariant)
                .selectinload(CartItem.variant)
                # ProductVariant -> product (Product)
                .selectinload(ProductVariant.product)
                # Product -> images (Image) فقط عکس اصلی
                .selectinload(Product.images),
                # فقط تصاویر is_primary=True را لود کن
                with_loader_criteria(
                    ProductImage,
                    ProductImage.is_primary.is_(True),
                    include_aliases=True,
                ),
            )
        )

        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def create_cart(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id, status=CartStatus.ACTIVE)
        self.db.add(cart)

        return cart

    async def upsert_items(self, cart: Cart, items: list[dict]):
        # items => [{"variant_id": x, "qty": y}, ...]
        existing = {i.variant_id: i for i in cart.items}

        for item in items:
            if item["variant_id"] in existing:
                existing[item["variant_id"]].qty = item["qty"]
            else:
                self.db.add(
                    CartItem(
                        cart_id=cart.id, variant_id=item["variant_id"], qty=item["qty"]
                    )
                )

        self.db.commit()
        self.db.refresh(cart)
        return cart

    async def clear_cart(self, cart: Cart):
        cart.items.clear()
        self.db.commit()

    # ---------------------------
    # Unit of Work helpers
    # ---------------------------
    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, data: Cart):
        await self.db.refresh(data)
