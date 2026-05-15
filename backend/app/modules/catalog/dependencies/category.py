# app/modules/catalog/dependencies/category.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.services.category import (
    CategoryService,
    ProductCategoryService,
)


# --------------------------------------------------
# Category Dependency
# --------------------------------------------------
def get_category_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("category"))],
) -> CategoryService:

    return CategoryService(db=db, cache=cache)


# --------------------------------------------------
# Product Category Dependency
# --------------------------------------------------
def get_product_category_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("product_category"))],
) -> ProductCategoryService:

    return ProductCategoryService(db=db, cache=cache)
