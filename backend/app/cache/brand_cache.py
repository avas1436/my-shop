import json

from fastapi import Request
from redis.asyncio import Redis


class BrandCache:
    def __init__(self, request: Request):
        self._request = request
        self._controller = getattr(request.app.state, "redis", None)
        self._redis: Redis | None = None
        self._prefix: str = "brand"

        if self._controller:
            self._redis = getattr(self._controller, "redis_client", None)
            self._prefix = getattr(self._controller, "session_prefix", "") or ""

    # -------------------------
    # internal helpers
    # -------------------------
    def _key(self, key: str) -> str:
        # اگر prefix تعریف شده باشد به ابتدای کلید اضافه می‌شود
        return f"{self._prefix}{key}"

    def _brand_key(self, brand_id: int) -> str:
        return self._key(f"brand:{brand_id}")

    def _list_key(self, key: str) -> str:
        return self._key(key)

    def _ensure(self) -> Redis:
        if not self._redis:
            raise RuntimeError("Redis client is not initialized")
        return self._redis

    # -------------------------
    # Brand cache
    # -------------------------
    async def get_brand(self, brand_id: int) -> dict | None:
        redis = self._ensure()
        cached = await redis.get(self._brand_key(brand_id))
        return json.loads(cached) if cached else None

    async def set_brand(self, brand_id: int, payload: dict, ttl: int = 300) -> None:
        redis = self._ensure()
        await redis.setex(self._brand_key(brand_id), ttl, json.dumps(payload))

    # -------------------------
    # List cache
    # -------------------------
    async def get_list(self, key: str) -> dict | None:
        redis = self._ensure()
        cached = await redis.get(self._list_key(key))
        return json.loads(cached) if cached else None

    async def set_list(self, key: str, payload: dict, ttl: int = 120) -> None:
        redis = self._ensure()
        await redis.setex(self._list_key(key), ttl, json.dumps(payload))

    # -------------------------
    # Invalidate
    # -------------------------
    async def invalidate_brand(self, brand_id: int) -> None:
        redis = self._ensure()
        await redis.delete(self._brand_key(brand_id))

    async def invalidate_lists(self) -> None:
        redis = self._ensure()
        pattern = self._key("brand:list:*")
        keys = await redis.keys(pattern)
        if keys:
            await redis.delete(*keys)
