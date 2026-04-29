from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.tag import Tag


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
