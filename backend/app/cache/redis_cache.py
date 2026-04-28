import json
from collections.abc import Callable
from typing import Any

from fastapi import Request
from redis.asyncio import Redis

from app.config.settings import get_settings

settings = get_settings()


class RedisNotInitializedError(RuntimeError):
    pass


class RedisDecodeError(ValueError):
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

        self._dumps = serializer or (
            lambda x: json.dumps(x, ensure_ascii=False, default=str)
        )
        self._loads = deserializer or (lambda x: json.loads(x))

        if self._controller:
            self._redis = getattr(self._controller, "redis_client", None)

    # -------------------------
    # internal helpers
    # -------------------------
    def _ensure(self) -> Redis:
        if not self._redis:
            raise RedisNotInitializedError("Redis client is not initialized")
        return self._redis

    def _build_key(self, *parts: Any) -> str:
        """
        مثال:
        session_prefix="shop:"
        namespace="brand"
        parts=("item", 12)
        => "shop:brand:item:12"
        """
        clean_parts = [
            str(p).strip(":") for p in parts if p is not None and str(p) != ""
        ]
        body = ":".join(clean_parts)

        if self._namespace and body:
            full = f"{self._namespace}:{body}"
        elif self._namespace:
            full = self._namespace
        else:
            full = body

        base = self._base_prefix.rstrip(":")
        return f"{base}:{full}" if full else base

    def _list_key(self, key: str) -> str:
        """
        کلیدهای لیست:  {prefix}{namespace}:list:{key}
        """
        return self._build_key("list", key)

    # -------------------------
    # generic CRUD cache
    # -------------------------
    async def get(self, *key_parts: Any) -> Any | None:
        redis = self._ensure()
        raw = await redis.get(self._build_key(*key_parts))
        if not raw:
            return None
        try:
            return self._loads(raw)
        except Exception as e:
            raise RedisDecodeError(f"Failed to decode redis value: {e}") from e

    async def set(
        self,
        *key_parts: Any,
        payload: Any,
        ttl: int | None = None,
    ) -> None:
        redis = self._ensure()
        key = self._build_key(*key_parts)
        value = self._dumps(payload)

        if ttl is None:
            await redis.set(key, value)
        else:
            await redis.setex(key, ttl, value)

    # -------------------------
    # list cache
    # -------------------------
    async def get_list(self, key: str) -> Any | None:
        redis = self._ensure()
        raw = await redis.get(self._list_key(key))
        if not raw:
            return None
        try:
            return self._loads(raw)
        except Exception as e:
            raise RedisDecodeError(f"Failed to decode redis value: {e}") from e

    async def set_list(
        self,
        key: str,
        payload: Any,
        ttl: int | None = None,
    ) -> None:
        redis = self._ensure()
        value = self._dumps(payload)
        ex = self._list_ttl if ttl is None else ttl

        if ex is None:
            await redis.set(self._list_key(key), value)
        else:
            await redis.setex(self._list_key(key), ex, value)

    # -------------------------
    # invalidate
    # -------------------------
    async def invalidate_key(self, *key_parts: Any) -> None:
        redis = self._ensure()
        await redis.delete(self._build_key(*key_parts))

    async def invalidate_lists(self) -> int:
        redis = self._ensure()
        pattern = self._build_key("list", "*")
        keys = await redis.keys(pattern)
        if not keys:
            return 0
        return await redis.delete(*keys)
