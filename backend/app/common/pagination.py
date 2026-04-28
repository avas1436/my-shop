from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageMeta(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta
