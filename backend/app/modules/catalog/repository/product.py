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

    # ---------------------------
    # Check exist with Product Slug
    # ---------------------------
    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.db.execute(select(exists().where(Product.slug == slug)))
        return bool(result.scalar())

    # ---------------------------
    # Check exist with Product SKU
    # ---------------------------
    async def exists_by_sku(self, sku: str) -> bool:
        result = await self.db.execute(select(exists().where(Product.sku == sku)))
        return bool(result.scalar())

    # ---------------------------
    # Get a Product by ID
    # ---------------------------
    async def get_by_id(self, product_id: int) -> Product | None:
        stmt = (
            select(Product)
            .where(
                Product.id == product_id,
                # با وجود این قسمت حذف شده ها نمایش داده نمی شوند
                Product.deleted_at.is_(None),
            )
            .options(
                # one-to-one / many-to-one
                selectinload(Product.brand),
                # many-to-many / one-to-many
                selectinload(Product.categories),
                selectinload(Product.tags),
                selectinload(Product.images),
                # attributes روی خود محصول
                selectinload(Product.attribute_values).selectinload(
                    ProductAttribute.attribute
                ),
                # variants + attributes روی هر واریانت
                selectinload(Product.variants)
                .selectinload(ProductVariant.attribute_values)
                .selectinload(ProductVariantAttribute.attribute),
                # variants + inventory (برای رفع MissingGreenlet)
                selectinload(Product.variants).selectinload(ProductVariant.inventory),
                # variants + inventory یک روش دیگر ولی پرفورمنس کم
                # selectinload(Product.variants)
                # .selectinload(ProductVariant.inventory)
                # .selectinload(Inventory.variant),
            )
        )

        result = await self.db.execute(stmt)
        product = result.scalar_one_or_none()

        return product

    # ---------------------------
    # Create Product
    # ---------------------------
    async def create(self, product: Product) -> Product:
        self.db.add(product)

        return product

    # ---------------------------
    # Update Product
    # ---------------------------
    async def update(self, obj: Product) -> Product:
        self.db.add(obj)
        return obj

    # ---------------------------
    # Soft Delete a Product
    # ---------------------------
    async def soft_delete(self, product_id: int) -> bool:
        result = await self.db.execute(
            update(Product)
            .where(Product.id == product_id, Product.deleted_at.is_(None))
            .values(deleted_at=datetime.now(UTC), status=ProductStatus.INACTIVE)
            .execution_options(synchronize_session="fetch")
        )
        # await self.db.commit()

        return result.rowcount > 0

    # ---------------------------
    # Hard Delete a Product
    # ---------------------------
    async def hard_delete(self, product_id: int) -> bool:

        result = await self.db.execute(delete(Product).where(Product.id == product_id))
        # await self.db.commit()

        return result.rowcount > 0

    # ---------------------------
    # Unit of Work helpers
    # ---------------------------
    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, data: Product):
        await self.db.refresh(data)


# ---------------------------
# Show all of a Product Data
# ---------------------------
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
