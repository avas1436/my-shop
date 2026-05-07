# app/modules/catalog/dependencies/product.py
from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.services.product import AdminProductService


# --------------------------------------------------
# Admin Product Dependency
# --------------------------------------------------
def get_admin_product_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache(namespace="admin-product"))],
) -> AdminProductService:

    repo = AdminProductRepository(db)
    return AdminProductService(repo=repo, cache=cache)
