# app/modules/catalog/services/image.py
import uuid

from fastapi import HTTPException, Request

from app.cache.redis_cache import RedisCache
from app.core.storage import get_storage
from app.modules.catalog.models.image import ProductImage
from app.modules.catalog.repository.image import ImageRepository
from app.modules.catalog.schemas.image import GetImage, ImageUpdate


class ImageService:
    def __init__(self, repo: ImageRepository, request: Request):
        self.repo = repo
        self.storage = get_storage()
        self.cache = RedisCache(request)

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
            url=saved_key,
            alt_text=alt_text,
            is_primary=is_primary,
            sort_order=sort_order,
        )

        if self.cache.is_available():
            await self.cache.invalidate_lists()

        return await self.repo.create(obj)

    # -------------------------
    # get a image
    # -------------------------
    async def get_image(self, image_id: int) -> GetImage:
        if self.cache.is_available():
            cached = await self.cache.get("image", image_id)
            if cached is not None:
                return cached

        image = await self.repo.get(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="image not found.")

        payload = GetImage.model_validate(image).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("image", image_id, payload=payload)

        return payload

    # -------------------------
    # get list of prodct images
    # -------------------------
    async def get_product_images(
        self,
        product_id: int,
    ) -> list[GetImage]:

        if self.cache.is_available():
            cached = await self.cache.get(
                "list",
                "image",
                "product",
                product_id,
            )
            if cached is not None:
                return cached

        images = await self.repo.list_by_product(product_id)

        if not images:
            raise HTTPException(status_code=404, detail="images not found.")

        payload = [
            GetImage.model_validate(img).model_dump(mode="json") for img in images
        ]

        if self.cache.is_available():
            await self.cache.set(
                "list",
                "image",
                "product",
                product_id,
                payload=payload,
            )

        return payload

    # -------------------------
    # update a image
    # -------------------------
    async def update_image(
        self,
        image_id: int,
        data: ImageUpdate,
    ) -> GetImage:

        image = await self.repo.get(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="image not found.")

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(image, k, v)

        image = await self.repo.update(obj=image)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("image", image_id)

        return image

    # -------------------------
    # delete a image
    # -------------------------
    async def delete_image(self, image_id: int) -> None:

        image = await self.repo.get(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="image not found.")

        await self.storage.delete(image.url)
        await self.repo.delete(image)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("image", image_id)
