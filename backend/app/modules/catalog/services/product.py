# app/modules/catalog/services/product.py
import re
import uuid
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from app.cache.cache import RedisCache
from app.errors.errors import (
    BadRequest,
    Conflict,
    InternalServerError,
    NotFound,
    UnprocessableEntity,
)
from app.modules.catalog.models.product import Product
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.schemas.product import DraftProductCreate, ProductAdminRead


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
            raise BadRequest("Invalid product id.")

        if self.cache.is_available():
            cached = await self.cache.get(product_id)
            if cached is not None:
                return cached

        product = await self.repo.get_by_id_for_admin(product_id)

        if not product:
            raise NotFound("Product not found.")

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
            )

            product = await self.repo.create(product)

            await self.repo.commit()
            await self.repo.refresh(product)

            if self.cache.is_available():
                await self.cache.invalidate_lists()

            return product

        except IntegrityError:
            await self.repo.rollback()
            raise Conflict("Slug or SKU already exists.") from None

        except Conflict:
            await self.repo.rollback()
            raise

        except UnprocessableEntity:
            await self.repo.rollback()
            raise

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError("Failed to create product.") from exc

    # ---------------------------
    # Soft Delete a product
    # ---------------------------
    async def soft_delete_product(self, product_id: int) -> Product:
        if product_id < 1:
            raise BadRequest("Invalid product id.")

        product = await self.repo.get_by_id_little(id=product_id)

        if not product:
            raise NotFound("Product not found.")

        try:
            ok = await self.repo.soft_delete(product=product)
            await self.repo.commit()
            await self.repo.refresh(product)

            if ok is not None and self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("product", product_id)

            return ok

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError("Failed to delete product.") from exc

    # ---------------------------
    # Hard Delete a product
    # ---------------------------
    async def hard_delete_product(self, product_id: int) -> bool:
        if product_id < 1:
            raise BadRequest("Invalid product id.")

        product = await self.repo.get_by_id_little(id=product_id)

        if not product:
            raise NotFound("Product not found.")

        try:
            await self.repo.hard_delete(product)

            await self.repo.commit()

            if self.cache.is_available():
                await self.cache.invalidate_lists()
                await self.cache.invalidate_key("product", product_id)

            return True

        except Exception as exc:
            await self.repo.rollback()
            raise InternalServerError("Failed to delete product.") from exc
