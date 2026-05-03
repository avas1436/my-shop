# app/modules/catalog/repository/product.py
from datetime import UTC, datetime

from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.common.enums import ProductStatus
from app.modules.catalog.models.attribute import (
    ProductAttribute,
    ProductVariantAttribute,
)
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.variant import ProductVariant


class AdminProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================
    # Create Product
    # =========================================================
    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    # =========================================================
    # Show all of a Product Data
    # =========================================================
    # async def list_all(self) -> list[Product]:
    #     result = await self.db.execute(
    #         select(Product)
    #         .options(
    #             selectinload(Product.category),
    #             selectinload(Product.inventory),
    #             selectinload(Product.comments),
    #         )
    #         .order_by(Product.id.desc())
    #     )
    #     return list(result.scalars().all())

    # =========================================================
    # Get a Product by ID
    # =========================================================
    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            select(Product)
            .where(
                Product.id == product_id,
                # با وجود این قسمت حذف شده ها نمایش داده نمی شوند
                Product.deleted_at.is_(None),
            )
            .options(
                selectinload(Product.brand),
                selectinload(Product.categories),
                selectinload(Product.tags),
                selectinload(Product.images),
                selectinload(Product.inventory),
                # attributes روی خود محصول
                selectinload(Product.attribute_values).selectinload(
                    ProductAttribute.attribute
                ),
                # variants + attributes روی هر واریانت
                selectinload(Product.variants)
                .selectinload(ProductVariant.attribute_values)
                .selectinload(ProductVariantAttribute.attribute),
                selectinload(Product.comments),
            )
        )
        return result.scalar_one_or_none()

    # =========================================================
    # Soft Delete a Product
    # =========================================================
    async def soft_delete(self, product_id: int) -> bool:
        result = await self.db.execute(
            update(Product)
            .where(Product.id == product_id, Product.deleted_at.is_(None))
            .values(deleted_at=datetime.now(UTC), status=ProductStatus.INACTIVE)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.commit()
        return result.rowcount > 0

    # =========================================================
    # Check exist of Product Slug
    # =========================================================
    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.db.execute(select(exists().where(Product.slug == slug)))
        return bool(result.scalar())

    # =========================================================
    # Check exist of Product SKU
    # =========================================================
    async def exists_by_sku(self, sku: str) -> bool:
        result = await self.db.execute(select(exists().where(Product.sku == sku)))
        return bool(result.scalar())

    # =========================================================
    # Hard Delete a Product
    # =========================================================
    async def hard_delete(self, product_id: int) -> bool:
        result = await self.db.execute(delete(Product).where(Product.id == product_id))
        await self.db.commit()
        return result.rowcount > 0
