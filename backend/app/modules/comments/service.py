# app/modules/comments/service.py
from __future__ import annotations

from app.modules.comments.models import Comment
from app.modules.comments.repository import CommentRepository
from app.modules.comments.schemas import CommentCreate


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def create(self, payload: CommentCreate) -> Comment:
        comment = Comment(**payload.model_dump())
        return await self.repository.create(comment)

    async def list_by_product(self, product_id: int) -> list[Comment]:
        return await self.repository.list_by_product(product_id)
