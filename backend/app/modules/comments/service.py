# app/modules/comments/service.py
from __future__ import annotations

import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.errors.errors import (
    BadRequest,
    Conflict,
    InternalServerError,
    NotFound,
    UnprocessableEntity,
)
from app.modules.comments.models import Comment
from app.modules.comments.repository import CommentRepository
from app.modules.comments.schemas import CommentCreate, CommentRead, CommentUpdate


class CommentService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = CommentRepository(db)
        self.cache = cache

    # ---------------------------
    # Read
    # ---------------------------
    async def get_comment_by_id(self, comment_id: int) -> Comment:
        if comment_id < 1:
            raise BadRequest("Invalid comment id.")

        if self.cache.is_available():
            cached = await self.cache.get(comment_id)
            if cached is not None:
                return cached

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFound("Comment not found.")

        payload = CommentRead.model_validate(comment).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set(comment_id, payload=payload)

        return payload

    async def list_comments(
        self,
        page: int,
        size: int,
        user_id: int | None = None,
        product_id: int | None = None,
    ) -> PageResponse[dict]:

        if page < 1 or size < 1 or size > 100:
            raise BadRequest("Invalid pagination values.")

        if user_id is not None and user_id < 1:
            raise BadRequest("Invalid user id.")
        if product_id is not None and product_id < 1:
            raise BadRequest("Invalid product id.")

        if self.cache.is_available():
            cached = await self.cache.get_list("list", user_id, product_id, page, size)
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            user_id=user_id,
            product_id=product_id,
            page=page,
            size=size,
        )

        pages = math.ceil(total / size) if total else 1
        response_items = [
            CommentRead.model_validate(c).model_dump(mode="json") for c in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                user_id,
                product_id,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    # ---------------------------
    # Create
    # ---------------------------
    async def create_comment(self, data: CommentCreate) -> Comment:
        if not data:
            raise BadRequest("Comment data is required.")

        try:
            comment = Comment(**data.model_dump())
            comment = await self.repo.create(comment)

            await self.db.commit()
            await self.db.refresh(comment)

            if self.cache.is_available():
                await self.cache.invalidate_lists()

            return comment

        except Conflict:
            await self.db.rollback()
            raise

        except UnprocessableEntity:
            await self.db.rollback()
            raise

        except Exception as exc:
            await self.db.rollback()
            raise InternalServerError("Failed to create comment.") from exc

    # ---------------------------
    # Update
    # ---------------------------
    async def update_comment(self, comment_id: int, data: CommentUpdate) -> Comment:
        if comment_id < 1:
            raise BadRequest("Invalid comment id.")

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFound("Comment not found.")

        payload = data.model_dump(exclude_unset=True)
        if not payload:
            raise BadRequest("No fields to update.")

        try:
            for k, v in payload.items():
                setattr(comment, k, v)

            comment = await self.repo.update(comment)

            await self.db.commit()
            await self.db.refresh(comment)

            if self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("comment", comment_id)

            return comment
        except Conflict:
            await self.db.rollback()
            raise
        except UnprocessableEntity:
            await self.db.rollback()
            raise
        except Exception as exc:
            await self.db.rollback()
            raise InternalServerError("Failed to update comment.") from exc

    # ---------------------------
    # Delete
    # ---------------------------
    async def delete_comment(self, comment_id: int) -> None:
        if comment_id < 1:
            raise BadRequest("Invalid comment id.")

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFound("Comment not found.")

        try:
            await self.repo.delete(comment)

            await self.db.commit()

            if self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("comment", comment_id)
        except Exception as exc:
            await self.db.rollback()
            raise InternalServerError("Failed to delete comment.") from exc
