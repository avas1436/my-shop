# app/modules/catalog/dependencies/product.py
from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.repository.product import (
    AdminProductRepository,
    UserProductRepository,
)
from app.modules.catalog.services.product import AdminProductService, UserProductService


# --------------------------------------------------
# Admin Product Dependency
# --------------------------------------------------
def get_admin_product_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("catalog"))],
) -> AdminProductService:

    repo = AdminProductRepository(db)
    return AdminProductService(repo=repo, cache=cache)


# --------------------------------------------------
# User Product Dependency
# --------------------------------------------------
def get_user_product_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("catalog"))],
) -> UserProductService:

    repo = UserProductRepository(db)
    return UserProductService(repo=repo, cache=cache)
