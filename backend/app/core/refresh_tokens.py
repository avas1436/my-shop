from datetime import timedelta

from redis.asyncio import Redis

from app.config.settings import get_settings

settings = get_settings()


def get_refresh_token_ttl() -> timedelta:
    return timedelta(days=settings.refresh_token_expire_days)


def build_refresh_token_key(token_id: str) -> str:
    return f"{settings.session_prefix}:refresh:{token_id}"


async def store_refresh_token(
    redis_client: Redis | None,
    token_id: str,
    subject: str,
) -> None:
    if redis_client is None:
        return

    ttl = max(int(get_refresh_token_ttl().total_seconds()), 1)
    await redis_client.setex(build_refresh_token_key(token_id), ttl, subject)


async def is_refresh_token_active(
    redis_client: Redis | None,
    token_id: str,
    subject: str,
) -> bool:
    if redis_client is None:
        return True

    stored_subject = await redis_client.get(build_refresh_token_key(token_id))
    return stored_subject == subject


async def revoke_refresh_token(redis_client: Redis | None, token_id: str) -> None:
    if redis_client is None:
        return

    await redis_client.delete(build_refresh_token_key(token_id))
