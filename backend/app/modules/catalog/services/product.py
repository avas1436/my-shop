import re
import uuid

from app.modules.catalog.models.product import Product
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.schemas.product import DraftProductCreate


class AdminProductService:
    def __init__(self, repository: AdminProductRepository):
        self.repository = repository

    @staticmethod
    def _slugify(text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^0-9a-zA-Zآ-یءئؤچژگپ\s_-]", "", text)
        text = re.sub(r"\s+", "-", text)
        text = re.sub(r"-{2,}", "-", text)
        return text.strip("-") or "product"

    async def _generate_unique_slug(self, name: str) -> str:
        base = self._slugify(name)
        slug = base
        i = 1
        while await self.repository.exists_by_slug(slug):
            i += 1
            slug = f"{base}-{i}"
        return slug

    async def _generate_unique_sku(self) -> str:
        # نمونه: PRD-20260427-8HEX
        while True:
            candidate = f"PRD-{uuid.uuid4().hex[:10].upper()}"
            if not await self.repository.exists_by_sku(candidate):
                return candidate

    async def draft_create(self, payload: DraftProductCreate) -> Product:
        slug = await self._generate_unique_slug(payload.name)
        sku = await self._generate_unique_sku()

        product = Product(
            sku=sku,
            slug=slug,
            name=payload.name,
            description=payload.description,
            price=payload.price,
            discount_price=payload.discount_price,
            cost_price=payload.cost_price,
            tax_rate=payload.tax_rate,
            status=payload.status,
            is_featured=payload.is_featured,
            is_digital=payload.is_digital,
            weight=payload.weight,
            meta_title=payload.meta_title,
            meta_description=payload.meta_description,
            gtin=payload.gtin,
        )
        return await self.repository.create(product)

    async def soft_delete_product(self, product_id: int) -> bool:
        return await self.repository.soft_delete(product_id)
