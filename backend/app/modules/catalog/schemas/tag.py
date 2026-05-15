from datetime import datetime

from pydantic import BaseModel, Field


# --------------------------------------------------
# Tag Schemas
# --------------------------------------------------
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


# --------------------------------------------------
# Product Tag Schemas
# --------------------------------------------------
class ProductTagAttach(BaseModel):
    tag_ids: list[int] = Field(..., min_length=1)


class ProductTagDetach(BaseModel):
    tag_ids: list[int] = Field(..., min_length=1)


class ProductTagSync(BaseModel):
    tag_ids: list[int] = Field(default_factory=list)


class ProductTagResult(BaseModel):
    product_id: int
    attached: list[int]
    detached: list[int]
    current: list[int]
