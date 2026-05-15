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
            .where(Cart.user_id == user_id, Cart.status == CartStatus.ACTIVE)
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

    async def get_variants_map(
        self, variant_ids: list[int]
    ) -> dict[int, ProductVariant]:

        if not variant_ids:
            return {}

        stmt = (
            select(ProductVariant)
            .where(
                ProductVariant.id.in_(variant_ids), ProductVariant.is_active.is_(True)
            )
            .options(selectinload(ProductVariant.product))
        )

        res = await self.db.execute(stmt)
        variants = res.scalars().all()

        return {v.id: v for v in variants}

    async def upsert_items(self, cart: Cart, items: dict[int, int]) -> None:
        """
        items: {variant_id: qty,}
        """

        for vid, qty in items.items():
            self.db.add(CartItem(cart_id=cart.id, variant_id=vid, qty=qty))

    # ---------------------------
    # Unit of Work helpers
    # ---------------------------
    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, data: Cart):
        await self.db.refresh(data)
