from uuid import uuid4

from redis.asyncio import Redis

from app.config.settings import get_settings


settings = get_settings()


class SessionManager:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def create_session(self, user_id: int) -> str:
        session_id = str(uuid4())
        await self.redis.setex(
            f"session:{session_id}",
            settings.session_expire_seconds,
            str(user_id),
        )
        return session_id

    async def get_user_id(self, session_id: str) -> int | None:
        value = await self.redis.get(f"session:{session_id}")
        return int(value) if value else None

    async def delete_session(self, session_id: str) -> None:
        await self.redis.delete(f"session:{session_id}")
