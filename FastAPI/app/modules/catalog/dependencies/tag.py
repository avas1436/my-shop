# app/modules/catalog/dependencies/tag.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.services.tag import (
    ProductTagService,
    TagService,
)


# --------------------------------------------------
# Tag Dependency
# --------------------------------------------------
def get_tag_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("tag"))],
) -> TagService:

    return TagService(db=db, cache=cache)


# --------------------------------------------------
# Product Tag Dependency
# --------------------------------------------------
def get_product_tag_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("product_tag"))],
) -> ProductTagService:

    return ProductTagService(db=db, cache=cache)
