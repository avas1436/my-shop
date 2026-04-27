from datetime import UTC, datetime

from sqlalchemy import exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.catalog.models.product import Product


class AdminProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def list_all(self) -> list[Product]:
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.category),
                selectinload(Product.inventory),
                selectinload(Product.comments),
            )
            .order_by(Product.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.category), selectinload(Product.inventory))
        )
        return result.scalar_one_or_none()

    async def soft_delete(self, product_id: int) -> bool:
        result = await self.db.execute(
            update(Product)
            .where(Product.id == product_id, Product.deleted_at.is_(None))
            .values(deleted_at=datetime.now(UTC))
            .execution_options(synchronize_session="fetch")
        )
        await self.db.commit()
        return result.rowcount > 0

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.db.execute(select(exists().where(Product.slug == slug)))
        return bool(result.scalar())

    async def exists_by_sku(self, sku: str) -> bool:
        result = await self.db.execute(select(exists().where(Product.sku == sku)))
        return bool(result.scalar())
