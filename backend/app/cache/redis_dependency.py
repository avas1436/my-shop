from typing import Annotated

from fastapi import Depends, FastAPI, Request
from redis.asyncio import Redis

from app.cache.redis_cache import RedisCache
from app.config.settings import get_settings
from app.core.redis import RedisController

settings = get_settings()


class RedisNotInitializedError(RuntimeError):
    pass


# گرفتن ردیس مستقیم از اپ
def get_redis_from_app(app: FastAPI) -> Redis:

    controller = getattr(app.state, "redis", None)

    if controller is None or controller.redis_client is None:
        raise RedisNotInitializedError("Redis client is not initialized")

    return controller.redis_client


# برای روت‌ها (هنوز ریکویست دارد ولی فقط یک رپر است)
def get_redis(request: Request) -> Redis:
    return get_redis_from_app(request.app)


# گرفتن کش برای روت ها
def get_cache(
    namespace: str = "",
    default_ttl: int = 300,
    list_ttl: int = 120,
):
    """
    این یک
    Dependency Factory
    است و روش استفاده از آن به این صورت است:

    cache: RedisCache = Depends(get_cache("items", default_ttl=600))

    """

    def _dep(
        redis: Annotated[Redis, Depends(get_redis)],
    ) -> RedisCache:

        return RedisCache(
            redis=redis,
            namespace=namespace,
            default_ttl=default_ttl,
            list_ttl=list_ttl,
        )

    return _dep


# گرفتن ردیس برای ورکر یا صف
async def get_worker_redis():
    controller = await RedisController(
        redis_url=settings.redis_url,
        redis_max_connections=settings.redis_max_connections,
        redis_socket_timeout=settings.redis_socket_timeout,
        session_prefix=settings.session_prefix,
    ).init_redis()
    return controller
