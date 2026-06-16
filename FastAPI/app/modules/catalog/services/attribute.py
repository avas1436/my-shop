# app/modules/catalog/services/attribute.py
import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.core.utils import slugify
from app.errors.errors import BadRequest, Conflict, NotFound
from app.modules.catalog.models.attribute import (
    Attribute,
    ProductAttribute,
    ProductVariantAttribute,
)
from app.modules.catalog.repository.attribute import (
    AttributeRepository,
    ProductAttributeRepository,
    ProductVariantAttributeRepository,
)
from app.modules.catalog.schemas.attribute import (
    AttributeCreate,
    AttributeRead,
    AttributeUpdate,
    ProductAttributeCreate,
    ProductAttributeRead,
    ProductAttributeUpdate,
    ProductVariantAttributeCreate,
    ProductVariantAttributeRead,
    ProductVariantAttributeUpdate,
)


# --------------------------------------------------
# Attribute Service
# --------------------------------------------------
class AttributeService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = AttributeRepository(db)
        self.cache = cache

    async def create_attribute(self, data: AttributeCreate) -> Attribute:
        if await self.repo.get_by_name(data.name):
            raise Conflict(
                message="Attribute name already exists.",
                code="ATTRIBUTE_NAME_DUPLICATE",
            )

        slug = data.slug or slugify(data.name)
        if slug and await self.repo.get_by_slug(slug):
            raise Conflict(
                message="Attribute slug already exists.",
                code="ATTRIBUTE_SLUG_DUPLICATE",
            )

        attribute = Attribute(name=data.name, slug=slug)
        attribute = await self.repo.create(attribute)

        if self.cache.is_available():
            await self.cache.invalidate_lists()

        return attribute

    async def get_attribute(self, attribute_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("attribute", attribute_id)
            if cached is not None:
                return cached

        attribute = await self.repo.get_by_id(attribute_id)
        if not attribute:
            raise NotFound(
                message="Attribute not found.",
                code="ATTRIBUTE_NOT_FOUND",
            )

        payload = AttributeRead.model_validate(attribute).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("attribute", attribute_id, payload=payload)

        return payload

    async def list_attributes(
        self,
        page: int,
        size: int,
        search: str | None = None,
        attribute_id: int | None = None,
    ) -> PageResponse[dict]:

        if page < 1 or size < 1 or size > 100:
            raise BadRequest(
                message="Invalid pagination values.",
                code="PAGINATION_INVALID_VALUES",
            )

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list", "attribute", search, attribute_id, page, size
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            search=search,
            obj_id=attribute_id,
            page=page,
            size=size,
        )

        pages = math.ceil(total / size) if total else 1
        response_items = [
            {"id": a.id, "name": a.name, "slug": a.slug, "created_at": a.created_at}
            for a in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "attribute",
                search,
                attribute_id,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    async def update_attribute(
        self, attribute_id: int, data: AttributeUpdate
    ) -> Attribute:
        attribute = await self.repo.get_by_id(attribute_id)
        if not attribute:
            raise NotFound(message="Attribute not found.", code="ATTRIBUTE_NOT_FOUND")

        if data.name and data.name != attribute.name:
            if await self.repo.get_by_name(data.name):
                raise Conflict(
                    message="Attribute name already exists.",
                    code="ATTRIBUTE_NAME_DUPLICATE",
                )
            attribute.name = data.name

        if data.slug:
            if data.slug != attribute.slug and await self.repo.get_by_slug(data.slug):
                raise Conflict(
                    message="Attribute slug already exists.",
                    code="ATTRIBUTE_SLUG_DUPLICATE",
                )
            attribute.slug = data.slug

        attribute = await self.repo.update(attribute)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("attribute", attribute_id)

        return attribute

    async def delete_attribute(self, attribute_id: int) -> None:
        attribute = await self.repo.get_by_id(attribute_id)
        if not attribute:
            raise NotFound(message="Attribute not found.", code="ATTRIBUTE_NOT_FOUND")

        await self.repo.delete(attribute)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("attribute", attribute_id)


# --------------------------------------------------
# Product Attribute Service
# --------------------------------------------------
class ProductAttributeService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = ProductAttributeRepository(db)
        self.cache = cache

    async def create_product_attribute(
        self, data: ProductAttributeCreate
    ) -> ProductAttribute:
        if not await self.repo.product_exists(data.product_id):
            raise NotFound(message="Product not found.", code="PRODUCT_NOT_FOUND")
        if not await self.repo.attribute_exists(data.attribute_id):
            raise NotFound(message="Attribute not found.", code="ATTRIBUTE_NOT_FOUND")
        if await self.repo.get_by_pair(data.product_id, data.attribute_id):
            raise Conflict(
                message="Attribute already exists for product.",
                code="PRODUCT_ATTRIBUTE_DUPLICATE",
            )

        pa = ProductAttribute(
            product_id=data.product_id,
            attribute_id=data.attribute_id,
            value=data.value,
        )
        pa = await self.repo.create(pa)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("admin", "full")
            await self.cache.invalidate_key("user", "full")
            await self.cache.invalidate_key("user")
            await self.cache.invalidate_key("homepage")

        return pa

    async def get_product_attribute(self, pa_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("product_attribute", pa_id)
            if cached is not None:
                return cached

        pa = await self.repo.get_by_id(pa_id)
        if not pa:
            raise NotFound(
                message="Product attribute not found.",
                code="PRODUCT_ATTRIBUTE_NOT_FOUND",
            )

        payload = ProductAttributeRead.model_validate(pa).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("product_attribute", pa_id, payload=payload)

        return payload

    async def list_product_attributes(
        self,
        search: str | None,
        product_id: int | None,
        attribute_id: int | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:
        if page < 1 or size < 1 or size > 100:
            raise BadRequest(
                message="Invalid pagination values.",
                code="PAGINATION_INVALID_VALUES",
            )

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "product_attribute",
                search,
                product_id,
                attribute_id,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            search, product_id, attribute_id, page, size
        )

        pages = math.ceil(total / size) if total else 1
        response_items = [
            {
                "id": pa.id,
                "product_id": pa.product_id,
                "attribute_id": pa.attribute_id,
                "value": pa.value,
            }
            for pa in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "product_attribute",
                search,
                product_id,
                attribute_id,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    async def update_product_attribute(
        self, pa_id: int, data: ProductAttributeUpdate
    ) -> ProductAttribute:
        pa = await self.repo.get_by_id(pa_id)
        if not pa:
            raise NotFound(
                message="Product attribute not found.",
                code="PRODUCT_ATTRIBUTE_NOT_FOUND",
            )

        pa.value = data.value
        pa = await self.repo.update(pa)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_attribute", pa_id)
            await self.cache.invalidate_key("admin", "full")
            await self.cache.invalidate_key("user", "full")
            await self.cache.invalidate_key("user")
            await self.cache.invalidate_key("homepage")

        return pa

    async def delete_product_attribute(self, pa_id: int) -> None:
        pa = await self.repo.get_by_id(pa_id)
        if not pa:
            raise NotFound(
                message="Product attribute not found.",
                code="PRODUCT_ATTRIBUTE_NOT_FOUND",
            )

        await self.repo.delete(pa)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_attribute", pa_id)
            await self.cache.invalidate_key("admin", "full")
            await self.cache.invalidate_key("user", "full")
            await self.cache.invalidate_key("user")
            await self.cache.invalidate_key("homepage")


# --------------------------------------------------
# Product Variant Attribute Service
# --------------------------------------------------
class ProductVariantAttributeService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = ProductVariantAttributeRepository(db)
        self.cache = cache

    async def create_product_variant_attribute(
        self, data: ProductVariantAttributeCreate
    ) -> ProductVariantAttribute:
        if not await self.repo.variant_exists(data.variant_id):
            raise NotFound(message="Variant not found.", code="VARIANT_NOT_FOUND")
        if not await self.repo.attribute_exists(data.attribute_id):
            raise NotFound(message="Attribute not found.", code="ATTRIBUTE_NOT_FOUND")
        if await self.repo.get_by_pair(data.variant_id, data.attribute_id):
            raise Conflict(
                message="Attribute already exists for variant.",
                code="VARIANT_ATTRIBUTE_DUPLICATE",
            )

        pva = ProductVariantAttribute(
            variant_id=data.variant_id,
            attribute_id=data.attribute_id,
            value=data.value,
        )
        pva = await self.repo.create(pva)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_variant", data.variant_id)
            await self.cache.invalidate_key("admin", "full")
            await self.cache.invalidate_key("user", "full")
            await self.cache.invalidate_key("user")
            await self.cache.invalidate_key("homepage")

        return pva

    async def get_product_variant_attribute(self, pva_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("product_variant_attribute", pva_id)
            if cached is not None:
                return cached

        pva = await self.repo.get_by_id(pva_id)
        if not pva:
            raise NotFound(
                message="Variant attribute not found.",
                code="VARIANT_ATTRIBUTE_NOT_FOUND",
            )

        payload = ProductVariantAttributeRead.model_validate(pva).model_dump(
            mode="json"
        )

        if self.cache.is_available():
            await self.cache.set("product_variant_attribute", pva_id, payload=payload)

        return payload

    async def list_product_variant_attributes(
        self,
        search: str | None,
        variant_id: int | None,
        attribute_id: int | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:
        if page < 1 or size < 1 or size > 100:
            raise BadRequest(
                message="Invalid pagination values.",
                code="PAGINATION_INVALID_VALUES",
            )

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "product_variant_attribute",
                search,
                variant_id,
                attribute_id,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            search, variant_id, attribute_id, page, size
        )

        pages = math.ceil(total / size) if total else 1
        response_items = [
            {
                "id": pva.id,
                "variant_id": pva.variant_id,
                "attribute_id": pva.attribute_id,
                "value": pva.value,
            }
            for pva in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "product_variant_attribute",
                search,
                variant_id,
                attribute_id,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    async def update_product_variant_attribute(
        self, pva_id: int, data: ProductVariantAttributeUpdate
    ) -> ProductVariantAttribute:
        pva = await self.repo.get_by_id(pva_id)
        if not pva:
            raise NotFound(
                message="Variant attribute not found.",
                code="VARIANT_ATTRIBUTE_NOT_FOUND",
            )

        pva.value = data.value
        pva = await self.repo.update(pva)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_variant_attribute", pva_id)
            await self.cache.invalidate_key("product_variant", pva.variant_id)
            await self.cache.invalidate_key("admin", "full")
            await self.cache.invalidate_key("user", "full")
            await self.cache.invalidate_key("user")
            await self.cache.invalidate_key("homepage")

        return pva

    async def delete_product_variant_attribute(self, pva_id: int) -> None:
        pva = await self.repo.get_by_id(pva_id)
        if not pva:
            raise NotFound(
                message="Variant attribute not found.",
                code="VARIANT_ATTRIBUTE_NOT_FOUND",
            )

        await self.repo.delete(pva)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("product_variant_attribute", pva_id)
            await self.cache.invalidate_key("product_variant", pva.variant_id)
            await self.cache.invalidate_key("admin", "full")
            await self.cache.invalidate_key("user", "full")
            await self.cache.invalidate_key("user")
            await self.cache.invalidate_key("homepage")
