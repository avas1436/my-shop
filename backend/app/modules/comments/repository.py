# app/modules/comments/repository.py
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.comments.models import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------------
    # Read
    # ---------------------------
    async def get_by_id(self, id: int) -> Comment | None:
        stmt = select(Comment).where(Comment.id == id).limit(1)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_filtered(
        self,
        user_id: int | None,
        product_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[Comment], int]:

        query = select(Comment)
        count_query = select(func.count(Comment.id))

        if user_id is not None:
            query = query.where(Comment.user_id == user_id)
            count_query = count_query.where(Comment == user_id)

        if product_id is not None:
            query = query.where(Comment.product_id == product_id)
            count_query = count_query.where(Comment == product_id)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()

        return list(items), total

    # ---------------------------
    # Create
    # ---------------------------
    async def create(self, comment: Comment) -> Comment:
        self.db.add(comment)
        return comment

    # ---------------------------
    # Update
    # ---------------------------
    async def update(self, obj: Comment) -> Comment:
        self.db.add(obj)
        return obj

    # ---------------------------
    # Delete
    # ---------------------------
    async def delete(self, obj: Comment) -> None:
        await self.db.delete(obj)

    # ---------------------------
    # Unit of Work helpers
    # ---------------------------
    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, data: Comment):
        await self.db.refresh(data)
