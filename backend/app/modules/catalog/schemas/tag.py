from datetime import datetime

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str | None = Field(None, max_length=120)


class TagUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    slug: str | None = Field(None, max_length=120)


class TagRead(BaseModel):
    id: int
    name: str
    slug: str | None
    created_at: datetime

    class Config:
        from_attributes = True
