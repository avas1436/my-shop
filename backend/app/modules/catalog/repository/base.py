# app/modules/catalog/repository/base.py
from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, db: AsyncSession, model: type[ModelT]):
        self.db = db
        self.model = model

    async def get_by_id(self, obj_id: int) -> ModelT | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> ModelT | None:
        result = await self.db.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> ModelT | None:
        result = await self.db.execute(
            select(self.model).where(self.model.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        search: str | None,
        obj_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[ModelT], int]:
        query = select(self.model)
        count_query = select(func.count(self.model.id))

        if search:
            query = query.where(self.model.name.ilike(f"%{search}%"))
            count_query = count_query.where(self.model.name.ilike(f"%{search}%"))

        if obj_id:
            query = query.where(self.model.id == obj_id)
            count_query = count_query.where(self.model.id == obj_id)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()

        return list(items), total

    async def create(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self.db.delete(obj)
        await self.db.commit()
