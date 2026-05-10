# app/modules/catalog/repository/product.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

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
    async def get_full_product(
        self,
        product_id: int | None = None,
        slug: str | None = None,
        include_deleted: bool = False,
    ) -> Product | None:

        stmt = select(Product)

        if product_id is not None and slug is not None:
            raise ValueError(
                "Provide either product_id or slug, not both",
            )
        elif product_id is not None:
            stmt = stmt.where(Product.id == product_id)
        elif slug is not None:
            stmt = stmt.where(Product.slug == slug)
        else:
            return None

        # فیلتر کردن رکوردهای حذف شده در صورت نیاز
        if not include_deleted:
            stmt = stmt.where(Product.deleted_at.is_(None))

        stmt = stmt.options(
            # برای رابطه To-one از جوین استفاده میکنیم
            joinedload(Product.brand),
            # استفاده از selectinload برای روابط To-Many
            selectinload(Product.categories),
            selectinload(Product.tags),
            selectinload(Product.images),
            # ویژگی‌های خود محصول
            selectinload(Product.attribute_values).joinedload(
                ProductAttribute.attribute
            ),
            # ادغام لودینگ‌های مربوط به Variants
            selectinload(Product.variants).options(
                # لود کردن inventory برای هر واریانت (اگر One-to-One است از joinedload استفاده کنید)
                joinedload(ProductVariant.inventory),
                # لود کردن ویژگی‌های هر واریانت
                selectinload(ProductVariant.attribute_values).joinedload(
                    ProductVariantAttribute.attribute
                ),
            ),
        )

        result = await self.db.execute(stmt)
        product = result.unique().scalar_one_or_none()

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
