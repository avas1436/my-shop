# app/modules/catalog/services/image.py
import uuid

from app.modules.catalog.repositories.image import ImageRepository

from app.core.storage import get_storage
from app.modules.catalog.models.image import ProductImage


class ImageService:
    def __init__(self, repo: ImageRepository):
        self.repo = repo
        self.storage = get_storage()

    # =========================================================
    # Add Image
    # =========================================================
    async def add_image(
        self,
        product_id: int,
        file,
        alt_text=None,
        is_primary=False,
        sort_order=0,
    ):

        ext = file.filename.split(".")[-1]
        file_key = f"products/{product_id}/{uuid.uuid4()}.{ext}"

        data = await file.read()
        saved_key = await self.storage.save(data, file_key, file.content_type)

        obj = ProductImage(
            product_id=product_id,
            file_key=saved_key,
            alt_text=alt_text,
            is_primary=is_primary,
            sort_order=sort_order,
        )

        return await self.repo.create(obj)

    # =========================================================
    # Update Image
    # =========================================================
    async def update_image(self, img: ProductImage, **fields):

        for k, v in fields.items():
            if v is not None:
                setattr(img, k, v)

        return await self.repo.update(img)

    # =========================================================
    # Delete Image
    # =========================================================
    async def delete_image(self, img: ProductImage):

        await self.storage.delete(img.file_key)
        await self.repo.delete(img)
