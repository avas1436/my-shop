# app/modules/catalog/dependencies/image.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.repository.image import ImageRepository
from app.modules.catalog.services.image import ImageService


# --------------------------------------------------
# Image Dependency
# --------------------------------------------------
def get_image_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("catalog"))],
) -> ImageService:

    repo = ImageRepository(db)
    return ImageService(repo=repo, cache=cache)
