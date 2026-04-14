from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.comments.models import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def list_by_product(self, product_id: int) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.product_id == product_id).order_by(Comment.id.desc())
        )
        return list(result.scalars().all())
