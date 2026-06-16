# app/modules/catalog/dependencies/variant.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.services.variant import ProductVariantService


def get_product_variant_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("catalog"))],
) -> ProductVariantService:
    return ProductVariantService(db=db, cache=cache)
