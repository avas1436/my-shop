# app/modules/comments/schemas.py
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    rating: int = Field(default=5, ge=1, le=5)
    content: str | None = Field(min_length=1, max_length=3000)
    author_name: str = Field(min_length=2, max_length=255)


class CommentCreate(CommentBase):
    product_id: int
    user_id: int


class CommentUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    content: str | None = Field(default=None, min_length=1)
    author_name: str | None = Field(default=None, min_length=2, max_length=255)


class CommentRead(CommentBase):
    id: int
    product_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
