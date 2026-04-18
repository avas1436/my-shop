from collections.abc import AsyncIterator
from typing import Optional

from redis.asyncio import Redis, ConnectionPool


class RedisController:
    def __init__(
        self,
        redis_url: str,
        redis_max_connections: int,
        redis_socket_timeout: int,
        session_prefix: str,
    ) -> None:

        self.redis_url = redis_url
        self.redis_max_connections = redis_max_connections
        self.redis_socket_timeout = redis_socket_timeout
        self.session_prefix = session_prefix
        self.redis_pool: Optional[ConnectionPool] = None
        self.redis_client: Optional[Redis] = None

    # -------------------------------------------------------------
    # Initialize Redis
    # -------------------------------------------------------------
    async def init_redis(self):
        self.redis_pool = ConnectionPool.from_url(
            self.redis_url,
            max_connections=self.redis_max_connections,
            socket_timeout=self.redis_socket_timeout,
            decode_responses=True,  # return str instead of bytes
        )

        self.redis_client = Redis(connection_pool=self.redis_pool)

        return self

    # -------------------------------------------------------------
    # ShoutDown Redis
    # -------------------------------------------------------------
    async def close_redis(self):

        if self.redis_client:
            await self.redis_client.close()

        if self.redis_pool:
            await self.redis_pool.disconnect()

    # -------------------------------------------------------------
    # Get Redis
    # -------------------------------------------------------------
    async def get_redis(self) -> AsyncIterator[Redis]:
        if self.redis_client:
            yield self.redis_client
