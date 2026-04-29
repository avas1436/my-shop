from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.attribute import (
    Attribute,
    ProductAttribute,
    ProductVariantAttribute,
)
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.variant import ProductVariant


# --------------------------------------------------
# Attribure Repository
# --------------------------------------------------
class AttributeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, attribute_id: int) -> Attribute | None:
        result = await self.db.execute(
            select(Attribute).where(Attribute.id == attribute_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Attribute | None:
        result = await self.db.execute(select(Attribute).where(Attribute.name == name))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Attribute | None:
        result = await self.db.execute(select(Attribute).where(Attribute.slug == slug))
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        search: str | None,
        attribute_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[Attribute], int]:
        query = select(Attribute)
        count_query = select(func.count(Attribute.id))

        if search:
            query = query.where(Attribute.name.ilike(f"%{search}%"))
            count_query = count_query.where(Attribute.name.ilike(f"%{search}%"))

        if attribute_id:
            query = query.where(Attribute.id == attribute_id)
            count_query = count_query.where(Attribute.id == attribute_id)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()

        return list(items), total

    async def create(self, attribute: Attribute) -> Attribute:
        self.db.add(attribute)
        await self.db.commit()
        await self.db.refresh(attribute)
        return attribute

    async def update(self, attribute: Attribute) -> Attribute:
        self.db.add(attribute)
        await self.db.commit()
        await self.db.refresh(attribute)
        return attribute

    async def delete(self, attribute: Attribute) -> None:
        await self.db.delete(attribute)
        await self.db.commit()


# --------------------------------------------------
# Product Attribure Repository
# --------------------------------------------------
class ProductAttributeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def product_exists(self, product_id: int) -> bool:
        q = select(Product.id).where(Product.id == product_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def attribute_exists(self, attribute_id: int) -> bool:
        q = select(Attribute.id).where(Attribute.id == attribute_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def get_by_id(self, pa_id: int) -> ProductAttribute | None:
        result = await self.db.execute(
            select(ProductAttribute).where(ProductAttribute.id == pa_id)
        )
        return result.scalar_one_or_none()

    async def get_by_pair(
        self, product_id: int, attribute_id: int
    ) -> ProductAttribute | None:
        q = select(ProductAttribute).where(
            ProductAttribute.product_id == product_id,
            ProductAttribute.attribute_id == attribute_id,
        )
        result = await self.db.execute(q)
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        search: str | None,
        product_id: int | None,
        attribute_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[ProductAttribute], int]:
        query = select(ProductAttribute)
        count_query = select(func.count(ProductAttribute.id))

        if search:
            query = query.where(ProductAttribute.value.ilike(f"%{search}%"))
            count_query = count_query.where(ProductAttribute.value.ilike(f"%{search}%"))

        if product_id:
            query = query.where(ProductAttribute.product_id == product_id)
            count_query = count_query.where(ProductAttribute.product_id == product_id)

        if attribute_id:
            query = query.where(ProductAttribute.attribute_id == attribute_id)
            count_query = count_query.where(
                ProductAttribute.attribute_id == attribute_id
            )

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()
        return list(items), total

    async def create(self, pa: ProductAttribute) -> ProductAttribute:
        self.db.add(pa)
        await self.db.commit()
        await self.db.refresh(pa)
        return pa

    async def update(self, pa: ProductAttribute) -> ProductAttribute:
        self.db.add(pa)
        await self.db.commit()
        await self.db.refresh(pa)
        return pa

    async def delete(self, pa: ProductAttribute) -> None:
        await self.db.delete(pa)
        await self.db.commit()


# --------------------------------------------------
# Product Variant Attribure Repository
# --------------------------------------------------
class ProductVariantAttributeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def variant_exists(self, variant_id: int) -> bool:
        q = select(ProductVariant.id).where(ProductVariant.id == variant_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def attribute_exists(self, attribute_id: int) -> bool:
        q = select(Attribute.id).where(Attribute.id == attribute_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def get_by_id(self, pva_id: int) -> ProductVariantAttribute | None:
        result = await self.db.execute(
            select(ProductVariantAttribute).where(ProductVariantAttribute.id == pva_id)
        )
        return result.scalar_one_or_none()

    async def get_by_pair(
        self, variant_id: int, attribute_id: int
    ) -> ProductVariantAttribute | None:
        q = select(ProductVariantAttribute).where(
            ProductVariantAttribute.variant_id == variant_id,
            ProductVariantAttribute.attribute_id == attribute_id,
        )
        result = await self.db.execute(q)
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        search: str | None,
        variant_id: int | None,
        attribute_id: int | None,
        page: int,
        size: int,
    ) -> tuple[list[ProductVariantAttribute], int]:
        query = select(ProductVariantAttribute)
        count_query = select(func.count(ProductVariantAttribute.id))

        if search:
            query = query.where(ProductVariantAttribute.value.ilike(f"%{search}%"))
            count_query = count_query.where(
                ProductVariantAttribute.value.ilike(f"%{search}%")
            )

        if variant_id:
            query = query.where(ProductVariantAttribute.variant_id == variant_id)
            count_query = count_query.where(
                ProductVariantAttribute.variant_id == variant_id
            )

        if attribute_id:
            query = query.where(ProductVariantAttribute.attribute_id == attribute_id)
            count_query = count_query.where(
                ProductVariantAttribute.attribute_id == attribute_id
            )

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()
        return list(items), total

    async def create(self, pva: ProductVariantAttribute) -> ProductVariantAttribute:
        self.db.add(pva)
        await self.db.commit()
        await self.db.refresh(pva)
        return pva

    async def update(self, pva: ProductVariantAttribute) -> ProductVariantAttribute:
        self.db.add(pva)
        await self.db.commit()
        await self.db.refresh(pva)
        return pva

    async def delete(self, pva: ProductVariantAttribute) -> None:
        await self.db.delete(pva)
        await self.db.commit()
