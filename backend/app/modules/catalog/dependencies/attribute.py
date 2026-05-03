# app/modules/catalog/dependencies/attribute.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.cache.redis_dependency import get_cache
from app.core.database import get_db
from app.modules.catalog.services.attribute import (
    AttributeService,
    ProductAttributeService,
    ProductVariantAttributeService,
)


# --------------------------------------------------
# Attribure Dependency
# --------------------------------------------------
def get_attribute_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("attribute"))],
) -> AttributeService:

    return AttributeService(db=db, cache=cache)


# --------------------------------------------------
# Product Attribure Dependency
# --------------------------------------------------
def get_product_attribute_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("product_attribute"))],
) -> ProductAttributeService:

    return ProductAttributeService(db=db, cache=cache)


# --------------------------------------------------
# Product Variant Attribure Dependency
# --------------------------------------------------
def get_product_variant_attribute_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    cache: Annotated[RedisCache, Depends(get_cache("product_variant_attribute"))],
) -> ProductVariantAttributeService:

    return ProductVariantAttributeService(db=db, cache=cache)
