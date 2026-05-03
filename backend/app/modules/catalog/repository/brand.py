# app/modules/catalog/repository/brand.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.brand import Brand
from app.modules.catalog.repository.base import BaseSimpleRepository


class BrandRepository(BaseSimpleRepository[Brand]):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Brand)
