# app/modules/comments/repository.py
from __future__ import annotations

from sqlalchemy import select
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

    async def list_by_user_id(self, user_id: str) -> list[Comment]:
        stmt = select(Comment).where(Comment.user_id == user_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def list_by_product_id(self, product_id: str) -> list[Comment]:
        stmt = (
            select(Comment)
            .where(Comment.product_id == product_id)
            .order_by(Comment.id.desc())
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

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
