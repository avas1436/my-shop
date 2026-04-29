# app/modules/catalog/repository/brand.py
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.brand import Brand


class BrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, brand_id: int) -> Brand | None:
        result = await self.db.execute(select(Brand).where(Brand.id == brand_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Brand | None:
        result = await self.db.execute(select(Brand).where(Brand.name == name))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Brand | None:
        result = await self.db.execute(select(Brand).where(Brand.slug == slug))
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        search: str | None,
        brand_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[Brand], int]:

        query = select(Brand)
        count_query = select(func.count(Brand.id))

        if search:
            query = query.where(Brand.name.ilike(f"%{search}%"))
            count_query = count_query.where(Brand.name.ilike(f"%{search}%"))

        if brand_id:
            query = query.where(Brand.id == brand_id)
            count_query = count_query.where(Brand.id == brand_id)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()

        return list(items), total

    async def create(self, brand: Brand) -> Brand:
        self.db.add(brand)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand

    async def update(self, brand: Brand) -> Brand:
        self.db.add(brand)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand

    async def delete(self, brand: Brand) -> None:
        await self.db.delete(brand)
        await self.db.commit()
