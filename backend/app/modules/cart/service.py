# app/modules/cart/service.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.errors.errors import BadRequest
from app.modules.cart.models import Cart
from app.modules.cart.repository import CartRepo


class CartService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = CartRepo(db)
        self.cache = cache

    async def _get_or_create_active_cart(self, user_id: int) -> Cart:
        cart = await self.repo.get_active_cart(user_id=user_id)
        if cart:
            return cart

        cart = await self.repo.create_cart(user_id=user_id)
        await self.db.commit()
        await self.db.refresh(cart)

        return cart

    async def finalize_to_db_async(
        self,
        user_id: int,
        items: dict[int, int],  # [variant_id: qty]
    ):

        if user_id < 1:
            raise BadRequest("Invalid user id.")

        if not items:
            raise BadRequest("Cart items cannot be empty.")

        # حذف مواردی که آیدی یا تعداد کمتر از 1 دارند
        valid_item: dict[int, int] = {
            vid: qty for vid, qty in items.items() if vid > 0 and qty > 0
        }

        # list of VIDs
        list_vid = list(vid for vid in valid_item.keys())

        # گرفتن قیمت‌های معتبر
        variants_map = await self.repo.get_variants_map(list_vid)

        if len(variants_map) != len(list_vid):
            missing = set(list_vid) - set(variants_map.keys())
            raise BadRequest(f"Invalid or inactive variant ids: {sorted(missing)}")

        cart = await self._get_or_create_active_cart(user_id=user_id)

        # آیتم‌ها داخل cart_items
        await self.repo.upsert_items(cart, variants_map)

        # محاسبه total_qty و total_amount
        total_qty = 0
        total_amount = 0

        for row in variants_map:
            v = variants_map[row["variant_id"]]
            qty = row["qty"]
            unit_price = v.final_price  # قیمت نهایی (با منطق product/variant)
            total_qty += qty
            total_amount += unit_price * qty

        await self.repo.set_cart_totals(
            cart=cart,
            total_amount=total_amount,
            total_qty=total_qty,
        )

        return cart

    async def get_cart(self, user_id: int):

        if self.cache.is_available():
            cart = await self.cache.get("cart", user_id)
            if cart is not None:
                return cart

        cart = self.repo.get_active_cart(user_id=user_id)

        if self.cache.is_available():
            cart = await self.cache.set("cart", user_id, payload=cart)

        return cart
