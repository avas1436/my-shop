# app/modules/comments/router.py
from __future__ import annotations

from app.api.v1.dependencies import get_db_session
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.comments.repository import CommentRepository
from app.modules.comments.schemas import CommentCreate, CommentRead
from app.modules.comments.service import CommentService

router = APIRouter()


@router.get("/", response_model=list[CommentRead])
async def list_comments(
    product_id: int = Query(...),
    db: AsyncSession = Depends(get_db_session),
) -> list[CommentRead]:
    service = CommentService(CommentRepository(db))
    comments = await service.list_by_product(product_id)
    return [CommentRead.model_validate(comment) for comment in comments]


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    payload: CommentCreate, db: AsyncSession = Depends(get_db_session)
) -> CommentRead:
    service = CommentService(CommentRepository(db))
    comment = await service.create(payload)
    return CommentRead.model_validate(comment)
