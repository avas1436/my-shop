# app/modules/users/dependencies.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.common.request_meta import ClientMeta, client_meta
from app.config.settings import get_settings
from app.core.database import get_db
from app.modules.users.service import AuthService

settings = get_settings()


# --------------------------------------------------
# Authentification Dependency
# --------------------------------------------------
def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("auth"))],
    meta: Annotated[ClientMeta, Depends(client_meta)],
) -> AuthService:

    ttl = settings.refresh_token_ttl

    return AuthService(db=db, cache=cache, meta=meta, ttl=ttl)
