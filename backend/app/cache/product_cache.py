import json

from redis.asyncio import Redis


class ProductCache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def get_product(self, product_id: int) -> dict | None:
        cached = await self.redis.get(f"product:{product_id}")
        return json.loads(cached) if cached else None

    async def set_product(self, product_id: int, payload: dict, ttl: int = 300) -> None:
        await self.redis.setex(f"product:{product_id}", ttl, json.dumps(payload))
