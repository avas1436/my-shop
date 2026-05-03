# app/modules/catalog/repository/tag.py
from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.product import Product
from app.modules.catalog.models.tag import ProductTag, Tag


# --------------------------------------------------
# Tag Repository
# --------------------------------------------------
class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tag_id: int) -> Tag | None:
        result = await self.db.execute(select(Tag).where(Tag.id == tag_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Tag | None:
        result = await self.db.execute(select(Tag).where(Tag.name == name))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Tag | None:
        result = await self.db.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        search: str | None,
        tag_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[Tag], int]:

        query = select(Tag)
        count_query = select(func.count(Tag.id))

        if search:
            query = query.where(Tag.name.ilike(f"%{search}%"))
            count_query = count_query.where(Tag.name.ilike(f"%{search}%"))

        if tag_id:
            query = query.where(Tag.id == tag_id)
            count_query = count_query.where(Tag.id == tag_id)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()

        return list(items), total

    async def create(self, tag: Tag) -> Tag:
        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag

    async def update(self, tag: Tag) -> Tag:
        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag

    async def delete(self, tag: Tag) -> None:
        await self.db.delete(tag)
        await self.db.commit()


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
