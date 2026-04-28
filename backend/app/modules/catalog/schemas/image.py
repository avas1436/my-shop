# app/modules/catalog/schemas/image.py
from pydantic import BaseModel


class GetImage(BaseModel):
    id: int
    product_id: int
    url: str
    alt_text: str | None
    is_primary: bool
    sort_order: int

    class Config:
        from_attributes = True


class ImageUpdate(BaseModel):
    alt_text: str | None = None
    is_primary: bool | None = None
    sort_order: int | None = None
