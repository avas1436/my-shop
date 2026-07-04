# app/modules/comments/service.py
from __future__ import annotations

import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.enums import UserRole
from app.common.pagination import PageMeta, PageResponse
from app.errors.errors import (
    BadRequest,
    Conflict,
    Forbidden,
    InternalServerError,
    NotFound,
    UnprocessableEntity,
)
from app.modules.comments.models import Comment
from app.modules.comments.repository import CommentRepository
from app.modules.comments.schemas import CommentCreate, CommentRead, CommentUpdate
from app.modules.users.models import User


class CommentService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = CommentRepository(db)
        self.cache = cache

    # ---------------------------
    # Read
    # ---------------------------
    async def get_comment_by_id(self, comment_id: int) -> Comment:
        if comment_id < 1:
            raise BadRequest(
                message="Invalid comment id.",
                code="INVALID_COMMENT_ID",
            )

        if self.cache.is_available():
            cached = await self.cache.get(comment_id)
            if cached is not None:
                return cached

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFound(
                message="Comment not found.",
                code="COMMENT_NOT_FOUND",
            )

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
            raise BadRequest(
                message="Invalid pagination values.",
                code="COMMENT_PAGINATION_INVALID_VALUES",
            )

        if user_id is not None and user_id < 1:
            raise BadRequest(
                message="Invalid user id.",
                code="COMMENT_USER_INVALID_ID",
            )

        if product_id is not None and product_id < 1:
            raise BadRequest(
                message="Invalid product id.",
                code="COMMENT_PRODUCT_INVALID_ID",
            )

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
    async def create_comment(
        self, data: CommentCreate, user_id: int, product_id: int
    ) -> Comment:

        try:
            comment = Comment(
                **data.model_dump(),
                user_id=user_id,
                product_id=product_id,
            )
            comment = await self.repo.create(comment)

            await self.repo.commit()
            await self.repo.refresh(comment)

            if self.cache.is_available():
                await self.cache.invalidate_lists()

            return comment

        except Conflict:
            await self.repo.rollback()
            raise

        except UnprocessableEntity:
            await self.repo.rollback()
            raise

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to create comment.",
                code="COMMENT_CREATE_FAILED",
            ) from exc

    # ---------------------------
    # Update
    # ---------------------------
    async def update_comment(
        self, comment_id: int, data: CommentUpdate, user: User
    ) -> Comment:
        if comment_id < 1:
            raise BadRequest(
                message="Invalid comment id.",
                code="COMMENT_INVALID_ID",
            )

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFound(
                message="Comment not found.",
                code="COMMENT_NOT_FOUND",
            )

        if user.role != UserRole.ADMIN or comment.user_id != user.id:
            raise Forbidden(
                message="Cant change this comment",
                code="COMMENT_ACCESS_DENIED",
            )

        payload = data.model_dump(exclude_unset=True)
        if not payload:
            raise BadRequest(
                message="No fields to update.",
                code="COMMENT_NO_FIELDS_TO_UPDATE",
            )

        try:
            for k, v in payload.items():
                setattr(comment, k, v)

            comment = await self.repo.update(comment)

            await self.repo.commit()
            await self.repo.refresh(comment)

            if self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("comment", comment_id)

            return comment
        except Conflict:
            await self.repo.rollback()
            raise
        except UnprocessableEntity:
            await self.repo.rollback()
            raise
        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to update comment.",
                code="COMMENT_UPDATE_FAILED",
            ) from exc

    # ---------------------------
    # Delete
    # ---------------------------
    async def delete_comment(self, comment_id: int, user: User) -> None:
        if comment_id < 1:
            raise BadRequest(
                message="Invalid comment id.",
                code="COMMENT_INVALID_ID",
            )

        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFound(
                message="Comment not found.",
                code="COMMENT_NOT_FOUND",
            )

        if user.role != UserRole.ADMIN or comment.user_id != user.id:
            raise Forbidden(
                message="Cant change this comment",
                code="COMMENT_ACCESS_DENIED",
            )

        try:
            await self.repo.delete(comment)

            await self.repo.commit()

            if self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("comment", comment_id)
        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to delete comment.",
                code="COMMENT_DELETE_FAILED",
            ) from exc
