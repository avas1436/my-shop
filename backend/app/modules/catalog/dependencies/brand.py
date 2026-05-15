# app/modules/catalog/dependencies/brand.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.services.brand import BrandService


# --------------------------------------------------
# Brand Dependency
# --------------------------------------------------
def get_brand_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("brand"))],
) -> BrandService:

    return BrandService(db=db, cache=cache)
