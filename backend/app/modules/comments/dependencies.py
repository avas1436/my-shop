# app/modules/comments/dependencies.py
from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.comments.service import CommentService


# --------------------------------------------------
# Comment Dependency
# --------------------------------------------------
def get_comment_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache(namespace="comment"))],
) -> CommentService:

    return CommentService(db=db, cache=cache)
