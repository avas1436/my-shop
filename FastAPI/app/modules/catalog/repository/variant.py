# app/modules/catalog/repository/variant.py
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.product import Product
from app.modules.catalog.models.variant import ProductVariant
from app.modules.catalog.repository.base import BaseRepository


class ProductVariantRepository(BaseRepository[ProductVariant]):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=ProductVariant)

    async def get_by_sku(self, sku: str) -> ProductVariant | None:
        result = await self.db.execute(
            select(ProductVariant).where(ProductVariant.sku == sku)
        )
        return result.scalar_one_or_none()

    # async def product_exists(self, product_id: int) -> bool:
    #     q = select(Product.id).where(Product.id == product_id)
    #     return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def get_product_price(self, product_id: int) -> int:
        q = select(Product).where(Product.id == product_id)
        result = await self.db.execute(q)
        product = result.scalar_one_or_none()

        if not product:
            return None

        return product.final_price, product.sku

    async def list_filtered(
        self,
        search: str | None,
        product_id: int | None,
        is_active: bool | None,
        page: int,
        size: int,
    ) -> tuple[list[ProductVariant], int]:
        query = select(ProductVariant)
        count_query = select(func.count(ProductVariant.id))

        if search:
            query = query.where(ProductVariant.sku.ilike(f"%{search}%"))
            count_query = count_query.where(ProductVariant.sku.ilike(f"%{search}%"))

        if product_id:
            query = query.where(ProductVariant.product_id == product_id)
            count_query = count_query.where(ProductVariant.product_id == product_id)

        if is_active is not None:
            query = query.where(ProductVariant.is_active == is_active)
            count_query = count_query.where(ProductVariant.is_active == is_active)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()
        return list(items), total
