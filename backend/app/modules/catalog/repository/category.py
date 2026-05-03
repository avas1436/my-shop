# app/modules/catalog/repository/catogory.py
from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.category import Category, ProductCategory
from app.modules.catalog.models.product import Product


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Category | None:
        result = await self.db.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Category | None:
        result = await self.db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    async def has_children(self, category_id: int) -> bool:
        result = await self.db.execute(
            select(func.count(Category.id)).where(Category.parent_id == category_id)
        )
        return (result.scalar_one() or 0) > 0

    async def list_filtered(
        self,
        search: str | None,
        parent_id: int | None,
        is_active: bool | None,
        page: int,
        size: int,
    ) -> tuple[list[Category], int]:

        query = select(Category)
        count_query = select(func.count(Category.id))

        if search:
            query = query.where(Category.name.ilike(f"%{search}%"))
            count_query = count_query.where(Category.name.ilike(f"%{search}%"))

        if parent_id is not None:
            query = query.where(Category.parent_id == parent_id)
            count_query = count_query.where(Category.parent_id == parent_id)

        if is_active is not None:
            query = query.where(Category.is_active == is_active)
            count_query = count_query.where(Category.is_active == is_active)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()

        return list(items), total

    async def create(self, category: Category) -> Category:
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category: Category) -> Category:
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        await self.db.delete(category)
        await self.db.commit()


class ProductCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def product_exists(self, product_id: int) -> bool:
        q = select(Product.id).where(Product.id == product_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def existing_categories(self, category_ids: list[int]) -> set[int]:
        if not category_ids:
            return set()
        q = select(Category.id).where(Category.id.in_(category_ids))
        rows = (await self.db.execute(q)).scalars().all()
        return set(rows)

    async def current_categories(self, product_id: int) -> set[int]:
        q = select(ProductCategory.category_id).where(
            ProductCategory.product_id == product_id
        )
        rows = (await self.db.execute(q)).scalars().all()
        return set(rows)

    async def add_links(self, product_id: int, category_ids: list[int]) -> None:
        if not category_ids:
            return
        values = [
            {"product_id": product_id, "category_id": cid} for cid in category_ids
        ]
        await self.db.execute(insert(ProductCategory), values)
        await self.db.commit()

    async def remove_links(self, product_id: int, category_ids: list[int]) -> None:
        if not category_ids:
            return
        q = delete(ProductCategory).where(
            ProductCategory.product_id == product_id,
            ProductCategory.category_id.in_(category_ids),
        )
        await self.db.execute(q)
        await self.db.commit()
