# app/modules/catalog/dependencies/product.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.services.product import AdminProductService


# --------------------------------------------------
# Admin Product Dependency
# --------------------------------------------------
def get_admin_product_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AdminProductService:

    repo = AdminProductRepository(db)
    return AdminProductService(repository=repo)
