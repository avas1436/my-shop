# app/modules/catalog/repository/image.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.image import ProductImage


class ImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================
    # Create Image
    # =========================================================
    async def create(self, obj: ProductImage) -> ProductImage:

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)

        return obj

    # =========================================================
    # Get Image
    # =========================================================
    async def get(self, image_id: int) -> ProductImage | None:

        res = await self.db.execute(
            select(ProductImage).where(ProductImage.id == image_id)
        )

        return res.scalars().first()

    # =========================================================
    # List All Images of a Product
    # =========================================================
    async def list_by_product(self, product_id: int):

        res = await self.db.execute(
            select(ProductImage)
            .where(ProductImage.product_id == product_id)
            .order_by(ProductImage.sort_order.asc())
        )

        return res.scalars().all()

    # =========================================================
    # Update Image
    # =========================================================
    async def update(self, obj: ProductImage) -> ProductImage:

        await self.db.commit()
        await self.db.refresh(obj)

        return obj

    # =========================================================
    # Delete Image
    # =========================================================
    async def delete(self, obj: ProductImage):

        await self.db.delete(obj)
        await self.db.commit()
