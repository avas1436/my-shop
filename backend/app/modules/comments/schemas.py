# app/modules/comments/schemas.py
from __future__ import annotations

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    product_id: int
    user_id: int
    rating: int = Field(ge=1, le=5)
    content: str
    author_name: str


class CommentRead(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    content: str
    author_name: str

    class Config:
        from_attributes = True
