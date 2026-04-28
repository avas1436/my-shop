# app/modules/catalog/schemas/image.py
from pydantic import BaseModel, field_serializer

from app.core.storage.generate_url import build_media_url


class GetImage(BaseModel):
    id: int
    product_id: int
    url: str
    alt_text: str | None
    is_primary: bool
    sort_order: int

    @field_serializer("url")
    def build_url(self, _):
        return build_media_url(self.url)

    class Config:
        from_attributes = True


class ImageUpdate(BaseModel):
    alt_text: str | None = None
    is_primary: bool | None = None
    sort_order: int | None = None
