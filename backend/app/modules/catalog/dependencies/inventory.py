from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.services.inventory import InventoryService


# --------------------------------------------------
# Inventory Dependency
# --------------------------------------------------
def get_inventory_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("inventory"))],
) -> InventoryService:

    return InventoryService(db=db, cache=cache)
