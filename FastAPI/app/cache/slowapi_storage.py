# app/cache/slowapi_storage.py
# این فایل قابلیت های اتمیک مناسب کنترل تعداد درخواست دارد

from limits.storage import MemoryStorage
from redis.asyncio import Redis


class RedisAsyncStorage(MemoryStorage):
    """
    Async Redis storage for SlowAPI.
    """

    def __init__(
        self,
        redis_client: Redis,
        prefix: str = "ratelimit:",
        expiration: int = 60,
    ):
        super().__init__()
        self._redis = redis_client
        self._prefix = prefix
        self._expiration = expiration

    def _make_key(self, key: str) -> str:
        """ساخت کلید کامل با prefix"""
        return f"{self._prefix}{key}"

    async def incr(
        self,
        key: str,
        expiration: int | None = None,
        connection: Redis | None = None,
    ) -> int:
        """افزایش شمارنده با TTL - Atomic operation"""
        redis = connection or self._redis
        full_key = self._make_key(key)
        ttl = expiration or self._expiration

        # استفاده از pipeline برای atomic operation
        async with redis.pipeline(transaction=True) as pipe:
            pipe.incr(full_key)
            if ttl:
                pipe.expire(full_key, ttl)
            results = await pipe.execute()

        return results[0]

    async def get(
        self,
        key: str,
        connection: Redis | None = None,
    ) -> int | None:
        """دریافت مقدار شمارنده"""
        redis = connection or self._redis
        full_key = self._make_key(key)
        value = await redis.get(full_key)
        return int(value) if value is not None else None

    async def reset(
        self,
        key: str,
        connection: Redis | None = None,
    ) -> None:
        """ریست کردن شمارنده"""
        redis = connection or self._redis
        full_key = self._make_key(key)
        await redis.delete(full_key)

    async def clear(
        self,
        connection: Redis | None = None,
    ) -> None:
        """پاک کردن تمام کلیدهای rate limit"""
        redis = connection or self._redis
        pattern = self._make_key("*")
        cursor = 0

        while True:
            cursor, keys = await redis.scan(
                cursor=cursor,
                match=pattern,
                count=100,
            )
            if keys:
                await redis.delete(*keys)
            if cursor == 0:
                break

    async def get_expiry(
        self,
        key: str,
        connection: Redis | None = None,
    ) -> int | None:
        """دریافت TTL باقی‌مانده"""
        redis = connection or self._redis
        full_key = self._make_key(key)
        return await redis.ttl(full_key)
