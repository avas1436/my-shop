import inspect
from collections.abc import Callable
from typing import Any

import orjson
from fastapi import Request
from redis.asyncio import Redis

from app.config.settings import get_settings

settings = get_settings()


class RedisNotInitializedError(RuntimeError):
    pass


class RedisDecodeError(ValueError):
    pass


class RedisInvalidKeyError(ValueError):
    pass


class RedisCache:
    def __init__(
        self,
        request: Request,
        namespace: str = "",
        default_ttl: int = 300,
        list_ttl: int = 120,
        serializer: Callable[[Any], str] | None = None,
        deserializer: Callable[[str], Any] | None = None,
    ):
        self._request = request
        self._controller = getattr(request.app.state, "redis", None)
        self._redis: Redis | None = None

        self._base_prefix: str = (settings.session_prefix or "").strip()

        self._namespace = namespace.strip(":")
        self._default_ttl = default_ttl
        self._list_ttl = list_ttl

        # خروجی serializer باید str باشد
        self._dumps = serializer or (lambda x: orjson.dumps(x).decode())

        # ورودی deserializer باید str باشد
        self._loads = deserializer or (lambda x: orjson.loads(x))

        if self._controller:
            self._redis = getattr(self._controller, "redis_client", None)

    # -------------------------
    # اطمینان از عملکرد درست ردیس
    # -------------------------
    def _ensure(self) -> Redis:
        if not self._redis:
            raise RedisNotInitializedError("Redis client is not initialized")
        return self._redis

    # -------------------------
    # تبدیل به بایت برای ذخیره در ردیس
    # -------------------------
    def _to_bytes(self, value: Any) -> bytes:
        if isinstance(value, bytes):
            return value
        if isinstance(value, bytearray):
            return bytes(value)
        if isinstance(value, str):
            return value.encode()
        # برای اطمینان، هر چیز دیگری را str کن
        return str(value).encode()

    # -------------------------
    # تبدیل به رشته برای دریافت از ردیس
    # -------------------------
    def _to_str(self, raw: Any) -> str:
        if isinstance(raw, str):
            return raw
        if isinstance(raw, (bytes, bytearray)):
            return raw.decode()
        # اگر چیزی غیر از این بود، str کن
        return str(raw)

    # -------------------------
    # ساخت کلید
    # -------------------------
    def _build_key(self, *parts: Any) -> str:
        """
        مثال:
        session_prefix="shop:"
        namespace="brand"
        parts=("item", 12)
        => "shop:brand:item:12"
        """
        clean_parts = []

        for p in parts:
            if p is None:
                continue
            s = str(p).strip(":")
            if s:
                clean_parts.append(s)

        body = ":".join(clean_parts)

        if self._namespace and body:
            full = f"{self._namespace}:{body}"
        elif self._namespace:
            full = self._namespace
        else:
            full = body

        base = self._base_prefix.rstrip(":")
        key = f"{base}:{full}" if full else base

        if not key:
            raise RedisInvalidKeyError("Redis key cannot be empty")

        return key

    # -------------------------
    # ساخت کلید برای لیست ها
    # -------------------------
    def _list_key(self, *parts: Any) -> str:
        """
        کلیدهای لیست:  {prefix}{namespace}:list:{key}
        """
        return self._build_key("list", *parts)

    # -------------------------
    # چک کردن عملکرد صحیح ردیس
    # -------------------------
    def is_available(self) -> bool:
        return self._redis is not None

    # -------------------------
    # get a key
    # -------------------------
    async def get(self, *key_parts: Any) -> Any | None:
        redis = self._ensure()
        raw = await redis.get(self._build_key(*key_parts))
        if raw is None:
            return None
        try:
            text = self._to_str(raw)
            return self._loads(text)
        except Exception as e:
            raise RedisDecodeError(f"Failed to decode redis value: {e}") from e

    # -------------------------
    # set a key
    # -------------------------
    async def set(
        self,
        *key_parts: Any,
        payload: Any,
        ttl: int | None = None,
    ) -> None:

        redis = self._ensure()
        key = self._build_key(*key_parts)
        text = self._dumps(payload)  # str
        value = self._to_bytes(text)  # bytes
        ttl = ttl if ttl is not None else self._default_ttl

        await redis.set(key, value, ex=ttl)

    # -------------------------
    # اگر مقدار داشته باشد میدهد اگر نه تابع را اجرا میکند و کلید را ذخیره میکند
    # -------------------------
    async def get_or_set(
        self,
        *key_parts: Any,
        ttl: int | None = None,
        factory: Callable[[], Any] | None = None,
    ):

        cached = await self.get(*key_parts)

        if cached is not None:
            return cached

        if factory is None:
            raise ValueError("factory is required")

        value = factory()

        if inspect.isawaitable(value):
            value = await value

        await self.set(*key_parts, payload=value, ttl=ttl)

        return value

    # -------------------------
    # get a list
    # -------------------------
    async def get_list(self, *parts: Any) -> Any | None:
        redis = self._ensure()
        raw = await redis.get(self._list_key(*parts))
        if raw is None:
            return None
        try:
            text = self._to_str(raw)
            return self._loads(text)
        except Exception as e:
            raise RedisDecodeError(f"Failed to decode redis value: {e}") from e

    # -------------------------
    # set a list
    # -------------------------
    async def set_list(
        self,
        *parts: Any,
        payload: Any,
        ttl: int | None = None,
    ) -> None:
        redis = self._ensure()
        text = self._dumps(payload)  # str
        value = self._to_bytes(text)  # bytes
        ex = self._list_ttl if ttl is None else ttl

        if ex is None:
            await redis.set(self._list_key(*parts), value)
        else:
            await redis.set(self._list_key(*parts), value, ex=ex)

    # -------------------------
    # invalidate single key
    # -------------------------
    async def invalidate_key(self, *key_parts: Any) -> None:
        redis = self._ensure()
        await redis.delete(self._build_key(*key_parts))

    # -------------------------
    # invalidate list key
    # -------------------------
    async def invalidate_lists(self) -> int:
        redis = self._ensure()
        pattern = self._build_key("list", "*")

        cursor = 0
        deleted = 0

        while True:
            cursor, batch = await redis.scan(
                cursor=cursor,
                match=pattern,
                count=100,
            )
            if batch:
                deleted += await redis.delete(*batch)
            if cursor == 0:
                break

        return deleted
