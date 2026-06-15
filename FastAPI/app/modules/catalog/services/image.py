# app/modules/catalog/services/image.py
import uuid

from app.cache.cache import RedisCache
from app.config import get_settings
from app.core.storage import get_storage
from app.errors.errors import BadRequest, NotFound
from app.modules.catalog.models.image import ProductImage
from app.modules.catalog.repository.image import ImageRepository
from app.modules.catalog.schemas.image import GetImage, ImageUpdate

settings = get_settings()


class ImageService:
    def __init__(self, repo: ImageRepository, cache: RedisCache):
        self.repo = repo
        self.storage = get_storage()
        self.cache = cache

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

        # بررسی فرمت فایل برای امنیت
        if ext not in settings.allowed_extensions:
            raise BadRequest(
                message="Invalid image format. Allowed formats are jpg, jpeg, png, webp.",
                code="IMAGE_INVALID_FORMAT",
            )

        data = await file.read()

        # بررسی حجم فایل
        if len(data) > settings.max_file_size:
            raise BadRequest(
                message="Image size exceeds the maximum limit of 5MB.",
                code="IMAGE_TOO_LARGE",
            )

        file_key = f"products/{product_id}/{uuid.uuid4()}.{ext}"

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
            raise NotFound(
                message="image not found.",
                code="IMAGE_NOT_FOUND",
            )

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
            cached = await self.cache.get_list(
                "list",
                "image",
                "product",
                product_id,
            )
            if cached is not None:
                return cached

        images = await self.repo.list_by_product(product_id)

        if not images:
            raise NotFound(
                message="No images found for this product.",
                code="PRODUCT_IMAGES_NOT_FOUND",
            )

        payload = [
            GetImage.model_validate(img).model_dump(mode="json") for img in images
        ]

        if self.cache.is_available():
            await self.cache.set_list(
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
            raise NotFound(
                message="image not found for update.",
                code="IMAGE_NOT_FOUND",
            )

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
            raise NotFound(
                message="image not found for deletion.",
                code="IMAGE_NOT_FOUND",
            )

        await self.storage.delete(image.url)
        await self.repo.delete(image)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("image", image_id)
