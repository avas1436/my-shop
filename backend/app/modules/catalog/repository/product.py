# app/modules/catalog/repository/product.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.catalog.models.attribute import (
    ProductAttribute,
    ProductVariantAttribute,
)
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.variant import ProductVariant
from app.modules.catalog.schemas.product import (
    ProductAdminUpdate,
    ProductPublish,
    ProductSoftDelete,
)


class AdminProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------------
    # Check exist with Product Slug
    # ---------------------------
    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(1).where(Product.slug == slug).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    # ---------------------------
    # Check exist with Product SKU
    # ---------------------------
    async def exists_by_sku(self, sku: str) -> bool:
        stmt = select(1).where(Product.sku == sku).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    # ---------------------------
    # Get a Product by ID (light)
    # ---------------------------
    async def get_by_id_little(self, id: int) -> Product:
        # این تابع تنها برای پرایمری کی است
        return await self.db.get(Product, id)

    # ---------------------------
    # Get a Product by ID (admin view)
    # ---------------------------
    async def get_by_id_for_admin(self, product_id: int) -> Product | None:
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
    async def update_product(
        self, product: Product, updates: ProductAdminUpdate
    ) -> Product:

        data = updates.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(product, field, value)

        self.db.add(product)

        return product

    # ---------------------------
    # Soft Delete Product
    # ---------------------------
    async def soflt_delete_product(
        self, product: Product, updates: ProductSoftDelete
    ) -> Product:

        data = updates.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(product, field, value)

        self.db.add(product)

        return product

    # ---------------------------
    # Published Product
    # ---------------------------
    async def published_product(
        self, product: Product, updates: ProductPublish
    ) -> Product:

        data = updates.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(product, field, value)

        self.db.add(product)

        return product

    # ---------------------------
    # Hard Delete a Product
    # ---------------------------
    async def hard_delete(self, obj: Product) -> None:
        await self.db.delete(obj)

    # ---------------------------
    # Unit of Work helpers
    # ---------------------------
    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, data: Product):
        await self.db.refresh(data)
