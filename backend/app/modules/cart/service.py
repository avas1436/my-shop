# app/modules/cart/service.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.core.redis import get_redis
from app.errors.errors import BadRequest
from app.modules.cart.models import Cart
from app.modules.cart.repository import CartRepo
from app.modules.cart.schemas import CartItemIn, CartOut


class CartService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = CartRepo(db)
        self.cache = cache

    # ---------------------------
    # Get from Redis
    # ---------------------------
    async def get_cart_redis(self, user_id: int) -> list[Cart]:

        redis = await get_redis()
        raw = await redis.get("cart", user_id)

        if not raw:
            return None

        payload = CartOut.model_validate(raw).model_dump(mode="json")

        return payload

    # ---------------------------
    # Set in Redis
    # ---------------------------
    async def set_cart_redis(
        self,
        user_id: int,
        payload: CartItemIn,
    ):
        if self.cache.is_available():
            await self.cache.set(
                "cart",
                user_id,
                payload.variant_id,
                payload=payload,
            )

    async def clear_cart_redis(self, user_id: int):
        if self.cache.is_available():
            await self.cache.invalidate_key("cart", user_id)

    async def remove_variant_from_redis(self, user_id: int, variant_id: int):
        if self.cache.is_available():
            await self.cache.invalidate_key("cart", user_id, variant_id)

    async def finalize_to_db_async(self, user_id: int):
        if user_id < 1:
            raise BadRequest("Invalid user id.")

        if self.cache.is_available():
            cart = await self.cache.get("cart", user_id)
            if cart is not None:
                return cart

        cart = self.repo.get_active_cart(user_id=user_id)

        if cart is not None:
            return cart

        cart = await self.repo.create_cart(user_id=user_id)

        self.db.commit()
        self.db.refresh(cart)

        return cart
