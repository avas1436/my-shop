# app/modules/catalog/services/variant.py
import math
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.errors.errors import BadRequest, Conflict, NotFound
from app.modules.catalog.models.variant import ProductVariant
from app.modules.catalog.repository.variant import ProductVariantRepository
from app.modules.catalog.schemas.variant import (
    ProductVariantCreate,
    ProductVariantRead,
    ProductVariantUpdate,
)


class ProductVariantService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = ProductVariantRepository(db)
        self.cache = cache

    # =========================================================
    # Make a Random name for SKU
    # =========================================================
    async def _generate_unique_sku(self) -> str:
        # نمونه: PRD-20260427-8HEX
        while True:
            candidate = f"PRD-{uuid.uuid4().hex[:5].upper()}"
            if not await self.repo.get_by_sku(candidate):
                return candidate

    async def create_variant(self, data: ProductVariantCreate) -> ProductVariant:
        if not await self.repo.product_exists(data.product_id):
            raise NotFound("Product not found.")

        sku = await self._generate_unique_sku()

        variant = ProductVariant(
            product_id=data.product_id,
            sku=sku,
            price=data.price,
            is_active=data.is_active,
        )
        variant = await self.repo.create(variant)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product", data.product_id)

        return variant

    async def get_variant(self, variant_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("product_variant", variant_id)
            if cached is not None:
                return cached

        variant = await self.repo.get_by_id(variant_id)
        if not variant:
            raise NotFound("Product variant not found.")

        payload = ProductVariantRead.model_validate(variant).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("product_variant", variant_id, payload=payload)

        return payload

    async def list_variants(
        self,
        search: str | None,
        product_id: int | None,
        is_active: bool | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:
        if page < 1 or size < 1 or size > 100:
            raise BadRequest("Invalid pagination values.")

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "product_variant",
                search,
                product_id,
                is_active,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            search, product_id, is_active, page, size
        )

        pages = math.ceil(total / size) if total else 1
        response_items = [
            {
                "id": v.id,
                "product_id": v.product_id,
                "sku": v.sku,
                "price": v.price,
                "is_active": v.is_active,
                "final_price": v.final_price,
            }
            for v in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "product_variant",
                search,
                product_id,
                is_active,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    async def update_variant(
        self, variant_id: int, data: ProductVariantUpdate
    ) -> ProductVariant:
        variant = await self.repo.get_by_id(variant_id)
        if not variant:
            raise NotFound("Product variant not found.")

        if data.sku and data.sku != variant.sku:
            if await self.repo.get_by_sku(data.sku):
                raise Conflict("Variant SKU already exists.")
            variant.sku = data.sku

        if data.price is not None:
            variant.price = data.price

        if data.is_active is not None:
            variant.is_active = data.is_active

        variant = await self.repo.update(variant)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_variant", variant_id)
            await self.cache.invalidate_key("product", variant.product_id)

        return variant

    async def delete_variant(self, variant_id: int) -> None:
        variant = await self.repo.get_by_id(variant_id)
        if not variant:
            raise NotFound("Product variant not found.")

        await self.repo.delete(variant)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_variant", variant_id)
            await self.cache.invalidate_key("product", variant.product_id)
