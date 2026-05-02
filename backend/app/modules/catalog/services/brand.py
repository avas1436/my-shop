# app/modules/catalog/services/brand.py
import math

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.core.utils import slugify
from app.modules.catalog.models.brand import Brand
from app.modules.catalog.repository.brand import BrandRepository
from app.modules.catalog.schemas.brand import BrandCreate, BrandRead, BrandUpdate


class BrandService:
    def __init__(self, db: AsyncSession, request: Request):
        self.repo = BrandRepository(db)
        self.cache = RedisCache(request)

    # -------------------------
    # create a brand
    # -------------------------
    async def create_brand(self, data: BrandCreate) -> Brand:

        if await self.repo.get_by_name(data.name):
            raise HTTPException(status_code=409, detail="Brand name already exists.")

        slug = data.slug or slugify(data.name)
        if slug and await self.repo.get_by_slug(slug):
            raise HTTPException(status_code=409, detail="Brand slug already exists.")

        brand = Brand(name=data.name, slug=slug)
        brand = await self.repo.create(brand)

        if self.cache.is_available():
            await self.cache.invalidate_lists()

        return brand

    # -------------------------
    # get a brand
    # -------------------------
    async def get_brand(self, brand_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("brand", brand_id)
            if cached is not None:
                return cached

        brand = await self.repo.get_by_id(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found.")

        payload = BrandRead.model_validate(brand).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("brand", brand_id, payload=payload)

        return payload

    # -------------------------
    # list brands
    # -------------------------
    async def list_brands(
        self,
        search: str | None,
        brand_id: int | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:

        if page < 1 or size < 1 or size > 100:
            raise HTTPException(status_code=400, detail="Invalid pagination values.")

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "brand",
                search,
                brand_id,
                page,
                size,
            )

            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(search, brand_id, page, size)

        pages = math.ceil(total / size) if total else 1
        response_items = []
        for b in items:
            response_items.append(
                {
                    "id": b.id,
                    "name": b.name,
                    "slug": b.slug,
                    "created_at": b.created_at,
                    "updated_at": b.updated_at,
                }
            )

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "brand",
                search,
                brand_id,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    # -------------------------
    # update a brand
    # -------------------------
    async def update_brand(self, brand_id: int, data: BrandUpdate) -> Brand:
        brand = await self.repo.get_by_id(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found.")

        if data.name and data.name != brand.name:
            if await self.repo.get_by_name(data.name):
                raise HTTPException(
                    status_code=409, detail="Brand name already exists."
                )
            brand.name = data.name

        if data.slug:
            if data.slug != brand.slug and await self.repo.get_by_slug(data.slug):
                raise HTTPException(
                    status_code=409, detail="Brand slug already exists."
                )
            brand.slug = data.slug

        brand = await self.repo.update(brand)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("brand", brand_id)

        return brand

    # -------------------------
    # delete a brand
    # -------------------------
    async def delete_brand(self, brand_id: int) -> None:
        brand = await self.repo.get_by_id(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found.")

        await self.repo.delete(brand)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("brand", brand_id)
