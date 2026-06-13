# app/modules/catalog/services/product.py
import math
import re
import uuid
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from app.cache.cache import RedisCache
from app.common.enums import ProductSortEnum, ProductStatus
from app.common.pagination import PageMeta, PageResponse
from app.errors.errors import (
    BadRequest,
    Conflict,
    InternalServerError,
    NotFound,
    UnprocessableEntity,
)
from app.modules.catalog.models.product import Product
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.schemas.product import (
    DraftProductCreate,
    ProductAdminRead,
    ProductAdminUpdate,
    ProductFullUserRead,
    ProductPublish,
    ProductSoftDelete,
    ProductUserLightRead,
)


# =========================================================
# Product Service for Admin
# =========================================================
class AdminProductService:
    def __init__(self, repo: AdminProductRepository, cache: RedisCache):
        self.repo = repo
        self.cache = cache

    # ---------------------------
    # Make slug from name
    # ---------------------------
    @staticmethod
    def _slugify(text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^0-9a-zA-Zآ-یءئؤچژگپ\s_-]", "", text)
        text = re.sub(r"\s+", "-", text)
        text = re.sub(r"-{2,}", "-", text)
        return text.strip("-") or "product"

    # ---------------------------
    # Add Number to duplicate slugs
    # ---------------------------
    async def _generate_unique_slug(self, name: str) -> str:
        base = self._slugify(name)
        slug = base
        i = 0
        while await self.repo.exists_by_slug(slug):
            i += 1
            slug = f"{base}-{i}"
        return slug

    # ---------------------------
    # Make a name for SKU
    # ---------------------------
    async def _generate_unique_sku(self) -> str:
        # نمونه: PRD-260501-A7K9
        today = datetime.now(UTC).strftime("%y%m%d")

        while True:
            rand = uuid.uuid4().hex[:4].upper()
            candidate = f"PRD-{today}-{rand}"

            if not await self.repo.exists_by_sku(candidate):
                return candidate

    # ---------------------------
    # Get a Product by ID for Admin show
    # ---------------------------
    async def get_product_admin(self, product_id: int) -> ProductAdminRead | None:
        if product_id < 1:
            raise BadRequest(
                message="Invalid product id.",
                code="PRODUCT_INVALID_ID",
            )

        if self.cache.is_available():
            cached = await self.cache.get(product_id)
            if cached is not None:
                return cached

        product = await self.repo.get_full_product(
            product_id=product_id,
            include_deleted=True,
        )

        if not product:
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        # payload = ProductAdminRead.model_validate(product).model_dump()
        payload = ProductAdminRead.model_validate(product).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set(product_id, payload=payload)

        obj = ProductAdminRead(**payload)

        return obj

    # ---------------------------
    # Create a Draft Product
    # ---------------------------
    async def draft_create(self, payload: DraftProductCreate) -> Product:
        slug = await self._generate_unique_slug(payload.name)
        sku = await self._generate_unique_sku()

        try:
            product = Product(
                sku=sku,
                slug=slug,
                name=payload.name,
                description=payload.description,
                price=payload.price,
                discount_price=payload.discount_price,
                cost_price=payload.cost_price,
                tax_rate=payload.tax_rate,
                is_digital=payload.is_digital,
                weight=payload.weight,
                meta_title=payload.meta_title,
                meta_description=payload.meta_description,
                gtin=payload.gtin,
                brand_id=payload.brand_id,
            )

            product = await self.repo.create(product)

            await self.repo.commit()
            await self.repo.refresh(product)

            if self.cache.is_available():
                await self.cache.invalidate_lists()

            return product

        except IntegrityError as e:
            await self.repo.rollback()
            raise Conflict(
                message=f"Data Validation Error: {e.orig}",
                code="PRODUCT_DATA_CONFLICT",
            ) from None

        except Conflict:
            await self.repo.rollback()
            raise

        except UnprocessableEntity:
            await self.repo.rollback()
            raise

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to create product.",
                code="PRODUCT_CREATE_FAILED",
            ) from exc

    # ---------------------------
    # Soft Delete a product
    # ---------------------------
    async def soft_delete_product(self, product_id: int) -> Product:
        if product_id < 1:
            raise BadRequest(
                message="Invalid product id.",
                code="PRODUCT_INVALID_ID",
            )

        product = await self.repo.get_by_id_little(id=product_id)

        if not product:
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        now = datetime.now(UTC)
        payload = ProductSoftDelete(
            deleted_at=now,
            status=ProductStatus.INACTIVE,
        )

        try:
            ok = await self.repo.soflt_delete_product(
                product=product,
                updates=payload,
            )

            await self.repo.commit()

            await self.repo.refresh(product)

            if ok is not None and self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("product", product_id)

            return ok

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message=f"Failed to delete product. {exc}",
                code="PRODUCT_DELETE_FAILED",
            ) from exc

    # ---------------------------
    # Hard Delete a product
    # ---------------------------
    async def hard_delete_product(self, product_id: int) -> bool:
        if product_id < 1:
            raise BadRequest(
                message="Invalid product id.",
                code="PRODUCT_INVALID_ID",
            )

        product = await self.repo.get_by_id_little(id=product_id)

        if not product:
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        try:
            await self.repo.hard_delete(product)

            await self.repo.commit()

            if self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("product", product_id)

            return True

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to delete product.",
                code="PRODUCT_HARD_DELETE_FAILED",
            ) from exc

    # ---------------------------
    # Update Product
    # ---------------------------
    async def update_product(
        self,
        product_id: int,
        updates: ProductAdminUpdate,
    ) -> Product:

        if product_id < 1:
            raise BadRequest(
                message="Invalid product id.",
                code="PRODUCT_INVALID_ID",
            )

        product = await self.repo.get_by_id_little(id=product_id)

        if not product:
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        try:
            ok = await self.repo.update_product(
                product=product,
                updates=updates,
            )

            await self.repo.commit()

            await self.repo.refresh(product)

            if ok is not None and self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("product", product_id)

            return ok

        except IntegrityError as e:
            await self.repo.rollback()
            raise Conflict(
                message=f"Data Validation Error: {e.orig}",
                code="PRODUCT_DATA_CONFLICT",
            ) from None

        except Conflict:
            await self.repo.rollback()
            raise

        except UnprocessableEntity:
            await self.repo.rollback()
            raise

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to update product.",
                code="PRODUCT_UPDATE_FAILED",
            ) from exc

    # ---------------------------
    # Published Product
    # ---------------------------
    async def published_product(
        self,
        product_id: int,
    ) -> Product:

        if product_id < 1:
            raise BadRequest(
                message="Invalid product id.",
                code="PRODUCT_INVALID_ID",
            )

        product = await self.repo.get_by_id_little(id=product_id)

        if not product:
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        if product.status == ProductStatus.INACTIVE or product.deleted_at is not None:
            raise UnprocessableEntity(
                message="Product is inactive or deleted.",
                code="PRODUCT_ALREADY_INACTIVE_OR_DELETED",
            )

        updates = ProductPublish(
            status=ProductStatus.ACTIVE,
            published_at=datetime.now(UTC),
        )

        try:
            ok = await self.repo.published_product(
                product=product,
                updates=updates,
            )

            await self.repo.commit()

            await self.repo.refresh(product)

            if ok is not None and self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("product", product_id)

            return ok

        except IntegrityError as e:
            await self.repo.rollback()
            raise Conflict(
                message=f"Data Validation Error: {e.orig}",
                code="PRODUCT_DATA_CONFLICT",
            ) from None

        except Conflict:
            await self.repo.rollback()
            raise

        except UnprocessableEntity:
            await self.repo.rollback()
            raise

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError(
                message="Failed to publish product.",
                code="PRODUCT_PUBLISH_FAILED",
            ) from exc


# =========================================================
# Product Service for User
# =========================================================
class UserProductService:
    def __init__(self, repo, cache: RedisCache):
        self.repo = repo
        self.cache = cache

    # ---------------------------------
    # Get Full Product (detail page)
    # ---------------------------------
    async def get_product_detail(
        self, product_id: int | None = None, slug: str | None = None
    ) -> ProductFullUserRead:

        if not product_id and not slug:
            raise BadRequest(
                message="product_id or slug is required",
                code="PRODUCT_IDENTIFIER_REQUIRED",
            )

        if product_id is not None:
            cache_key = f"product:{product_id}"
        elif slug is not None:
            cache_key = f"product:{slug}"

        if self.cache.is_available():
            cached = await self.cache.get(cache_key)

            if cached is not None:
                return ProductFullUserRead(**cached)

        product = await self.repo.get_full_product(
            product_id=product_id,
            slug=slug,
        )

        if not product:
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        payload = ProductFullUserRead.model_validate(product).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set(cache_key, payload=payload, ttl=500)

        return ProductFullUserRead(**payload)

    # ---------------------------------
    # List products (Light) - paginated
    # ---------------------------------
    async def search_products(
        self,
        *,
        q: str | None = None,
        brand_slugs: list[str] | None = None,
        category_slugs: list[str] | None = None,
        tag_slugs: list[str] | None = None,
        attribute_filters: dict[str, list[str]] | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        is_in_stock: bool | None = None,
        has_discount: bool | None = None,
        is_featured: bool | None = None,
        is_digital: bool | None = None,
        sort: ProductSortEnum | None = None,
        page: int = 1,
        size: int = 20,
    ) -> PageResponse[dict]:

        if page < 1 or size < 1 or size > 100:
            raise BadRequest(
                message="Invalid pagination values.",
                code="PAGINATION_INVALID_VALUES",
            )

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "product_search",
                q,
                brand_slugs,
                category_slugs,
                tag_slugs,
                attribute_filters,
                min_price,
                max_price,
                is_in_stock,
                has_discount,
                is_featured,
                is_digital,
                sort.value if sort else None,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        offset = (page - 1) * size

        items, total = await self.repo.list_light_advanced(
            text=q,
            brand_slugs=brand_slugs,
            category_slugs=category_slugs,
            tag_slugs=tag_slugs,
            attribute_filters=attribute_filters,
            min_price=min_price,
            max_price=max_price,
            is_in_stock=is_in_stock,
            has_discount=has_discount,
            is_featured=is_featured,
            is_digital=is_digital,
            sort=sort or ProductSortEnum.NEWEST,
            offset=offset,
            limit=size,
        )

        pages = math.ceil(total / size) if total else 1

        response_items = [
            ProductUserLightRead.model_validate(p).model_dump(mode="json")
            for p in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "product_search",
                q,
                brand_slugs,
                category_slugs,
                tag_slugs,
                attribute_filters,
                min_price,
                max_price,
                is_in_stock,
                has_discount,
                is_featured,
                is_digital,
                sort.value if sort else None,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    # ---------------------------
    # Home Page
    # ---------------------------
    async def get_homepage(
        self,
        *,
        limit: int = 12,
    ) -> list[ProductUserLightRead]:

        if self.cache.is_available():
            cached = await self.cache.get_list("homepage")
            if cached is not None:
                return [ProductUserLightRead(**i) for i in cached]

        items = await self.repo.get_homepage_featured(
            limit=limit,
            order_by_discount=True,
            order_by_newest=True,
        )

        response_items = [
            ProductUserLightRead.model_validate(p).model_dump(mode="json")
            for p in items
        ]

        if self.cache.is_available():
            await self.cache.set_list(
                "homepage",
                payload=response_items,
                ttl=1500,
            )

        return [ProductUserLightRead(**i) for i in response_items]
