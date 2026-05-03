# app/modules/catalog/repository/tag.py
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.product import Product
from app.modules.catalog.models.tag import ProductTag, Tag
from app.modules.catalog.repository.base import BaseRepository


# --------------------------------------------------
# Tag Repository
# --------------------------------------------------
class TagRepository(BaseRepository[Tag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Tag)


# --------------------------------------------------
# Product Tag Repository
# --------------------------------------------------
class ProductTagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def product_exists(self, product_id: int) -> bool:
        q = select(Product.id).where(Product.id == product_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def existing_tags(self, tag_ids: list[int]) -> set[int]:
        if not tag_ids:
            return set()
        q = select(Tag.id).where(Tag.id.in_(tag_ids))
        rows = (await self.db.execute(q)).scalars().all()
        return set(rows)

    async def current_tags(self, product_id: int) -> set[int]:
        q = select(ProductTag.tag_id).where(ProductTag.product_id == product_id)
        rows = (await self.db.execute(q)).scalars().all()
        return set(rows)

    async def add_links(self, product_id: int, tag_ids: list[int]) -> None:
        if not tag_ids:
            return
        values = [{"product_id": product_id, "tag_id": tid} for tid in tag_ids]
        await self.db.execute(insert(ProductTag), values)
        await self.db.commit()

    async def remove_links(self, product_id: int, tag_ids: list[int]) -> None:
        if not tag_ids:
            return
        q = delete(ProductTag).where(
            ProductTag.product_id == product_id,
            ProductTag.tag_id.in_(tag_ids),
        )
        await self.db.execute(q)
        await self.db.commit()
