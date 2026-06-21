# app/modules/catalog/services/category.py
import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.core.utils import slugify
from app.errors.errors import BadRequest, Conflict, NotFound
from app.modules.catalog.models.category import Category
from app.modules.catalog.repository.category import (
    CategoryRepository,
    ProductCategoryRepository,
)
from app.modules.catalog.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    ProductCategoryResult,
)


# --------------------------------------------------
# Category Service
# --------------------------------------------------
class CategoryService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = CategoryRepository(db)
        self.cache = cache

    # -------------------------
    # create a category
    # -------------------------
    async def create_category(self, data: CategoryCreate) -> Category:

        if await self.repo.get_by_name(data.name):
            raise Conflict(
                message="Category name already exists.",
                code="CATEGORY_NAME_DUPLICATE",
            )

        slug = data.slug or slugify(data.name)
        if slug and await self.repo.get_by_slug(slug):
            raise Conflict(
                message="Category slug already exists.",
                code="CATEGORY_SLUG_DUPLICATE",
            )

        parent_id = None
        if data.parent_id is not None:
            parent = await self.repo.get_by_id(data.parent_id)
            if not parent:
                raise NotFound(
                    message="Parent category not found.",
                    code="CATEGORY_PARENT_NOT_FOUND",
                )

            if not parent.is_active:
                raise BadRequest(
                    message="Cannot assign a category to an inactive parent.",
                    code="CATEGORY_PARENT_INACTIVE",
                )

            parent_id = data.parent_id

        category = Category(
            name=data.name,
            slug=slug,
            description=data.description,
            is_active=data.is_active,
            parent_id=parent_id,
        )
        category = await self.repo.create(category)

        if self.cache.is_available():
            await self.cache.invalidate_lists()

        return category

    # -------------------------
    # get a category
    # -------------------------
    async def get_category(self, category_id: int) -> dict:
        if self.cache.is_available():
            cached = await self.cache.get("category", category_id)
            if cached is not None:
                return cached

        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFound(
                message="Category not found.",
                code="CATEGORY_NOT_FOUND",
            )

        payload = CategoryRead.model_validate(category).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("category", category_id, payload=payload)

        return payload

    # -------------------------
    # list categories
    # -------------------------
    async def list_categories(
        self,
        search: str | None,
        parent_id: int | None,
        is_active: bool | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:

        if page < 1 or size < 1 or size > 100:
            raise BadRequest(
                message="Invalid pagination values.",
                code="CATEGORY_PAGINATION_INVALID",
            )

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "category",
                search,
                parent_id,
                is_active,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            search, parent_id, is_active, page, size
        )

        pages = math.ceil(total / size) if total > 0 else 1
        response_items = []
        for c in items:
            response_items.append(
                {
                    "id": c.id,
                    "name": c.name,
                    "slug": c.slug,
                    "description": c.description,
                    "is_active": c.is_active,
                    "parent_id": c.parent_id,
                    "created_at": c.created_at,
                    "updated_at": c.updated_at,
                }
            )

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "category",
                search,
                parent_id,
                is_active,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    # -------------------------
    # update a category
    # -------------------------
    async def update_category(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFound(
                message="Category not found.",
                code="CATEGORY_NOT_FOUND",
            )

        update_data = data.model_dump(exclude_unset=True)

        # 1. بررسی و آپدیت Name
        if "name" in update_data:
            new_name = update_data["name"]
            if new_name and new_name != category.name:
                if await self.repo.get_by_name(new_name):
                    raise Conflict(
                        message="Category name already exists.",
                        code="CATEGORY_NAME_DUPLICATE",
                    )
                category.name = new_name

        # 2. بررسی و آپدیت Slug
        if "slug" in update_data:
            new_slug = update_data["slug"]
            if new_slug and new_slug != category.slug:
                if await self.repo.get_by_slug(new_slug):
                    raise Conflict(
                        message="Category slug already exists.",
                        code="CATEGORY_SLUG_DUPLICATE",
                    )
                category.slug = new_slug

        # 3. آپدیت Description (حتی اگر None یا همان null باشد)
        if "description" in update_data:
            category.description = update_data["description"]

        # 4. آپدیت Is Active
        if "is_active" in update_data:
            category.is_active = update_data["is_active"]

        # 5. بررسی و آپدیت Parent ID (مهم‌ترین بخش برای پشتیبانی از null شدن)
        if "parent_id" in update_data:
            new_parent_id = update_data["parent_id"]

            if new_parent_id is None:
                # اگر کاربر عمداً null فرستاده، دسته‌بندی تبدیل به ریشه می‌شود
                category.parent_id = None
            else:
                # اگر فرستاده شده و null نیست، بررسی‌های منطقی انجام می‌شود
                if new_parent_id == category.id:
                    raise Conflict(
                        message="Category cannot be its own parent.",
                        code="CATEGORY_SELF_PARENT",
                    )

                parent = await self.repo.get_by_id(new_parent_id)
                if not parent:
                    raise NotFound(
                        message="Parent category not found.",
                        code="CATEGORY_PARENT_NOT_FOUND",
                    )
                if not parent.is_active:
                    raise BadRequest(
                        message="Parent category is inactive.",
                        code="CATEGORY_PARENT_INACTIVE",
                    )

                # دریافت تمام والدهایِ دسته‌بندیِ والدِ جدید با یک کوئری
                parent_ancestor_ids = await self.repo.get_all_parents_ids(new_parent_id)

                # جلوگیری از ایجاد چرخه
                if category.id in parent_ancestor_ids:
                    raise Conflict(
                        message="Parent category cannot be a descendant (creates a cycle).",
                        code="CATEGORY_CYCLE_DETECTED",
                    )

                category.parent_id = new_parent_id

        category = await self.repo.update(category)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("category", category_id)

        return category

    # -------------------------
    # delete a category
    # -------------------------
    async def delete_category(self, category_id: int) -> None:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFound(
                message="Category not found.",
                code="CATEGORY_NOT_FOUND",
            )

        if await self.repo.has_children(category_id):
            raise Conflict(
                message="Cannot delete category with children.",
                code="CATEGORY_HAS_CHILDREN",
            )

        await self.repo.delete(category)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("category", category_id)

    # -------------------------
    # list parents of a category
    # -------------------------
    async def get_category_parents(self, category_id: int) -> list[dict]:
        # ۱. ابتدا مطمئن می‌شویم که خود این دسته‌بندی وجود دارد
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFound(
                message="Category not found.",
                code="CATEGORY_NOT_FOUND",
            )

        # ۲. واکشی لیست والدها از دیتابیس
        parents = await self.repo.get_all_parents(category_id)

        # ۳. تبدیل به دایرکتوری جهت مطابقت با ساختار خروجی شما
        response_items = []
        for p in parents:
            response_items.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "slug": p.slug,
                    "description": p.description,
                    "is_active": p.is_active,
                    "parent_id": p.parent_id,
                    "created_at": p.created_at,
                    "updated_at": p.updated_at,
                }
            )

        return response_items


# --------------------------------------------------
# Product Category Service
# --------------------------------------------------
class ProductCategoryService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.repo = ProductCategoryRepository(db)
        self.cache = cache

    async def attach(
        self, product_id: int, category_ids: list[int]
    ) -> ProductCategoryResult:

        if not await self.repo.product_exists(product_id):
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        existing = await self.repo.existing_categories(category_ids)
        missing = set(category_ids) - existing
        if missing:
            raise NotFound(
                message=f"Categories not found: {sorted(missing)}",
                code="PRODUCT_CATEGORY_MAPPED_NOT_FOUND",
            )

        current = await self.repo.current_categories(product_id)
        to_add = list(set(category_ids) - current)

        await self.repo.add_links(product_id, to_add)

        current = current | set(to_add)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("admin", "full", product_id)
            await self.cache.invalidate_key("user", "full", product_id)
            await self.cache.invalidate_key("user", product_id)
            await self.cache.invalidate_key("homepage")

        return ProductCategoryResult(
            product_id=product_id,
            attached=sorted(to_add),
            detached=[],
            current=sorted(current),
        )

    async def detach(
        self, product_id: int, category_ids: list[int]
    ) -> ProductCategoryResult:

        if not await self.repo.product_exists(product_id):
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        current = await self.repo.current_categories(product_id)
        to_remove = list(set(category_ids) & current)

        await self.repo.remove_links(product_id, to_remove)

        current = current - set(to_remove)

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("admin", "full", product_id)
            await self.cache.invalidate_key("user", "full", product_id)
            await self.cache.invalidate_key("user", product_id)
            await self.cache.invalidate_key("homepage")

        return ProductCategoryResult(
            product_id=product_id,
            attached=[],
            detached=sorted(to_remove),
            current=sorted(current),
        )

    async def sync(
        self, product_id: int, category_ids: list[int]
    ) -> ProductCategoryResult:

        if not await self.repo.product_exists(product_id):
            raise NotFound(
                message="Product not found.",
                code="PRODUCT_NOT_FOUND",
            )

        existing = await self.repo.existing_categories(category_ids)
        missing = set(category_ids) - existing
        if missing:
            raise NotFound(
                message=f"Categories not found: {sorted(missing)}",
                code="PRODUCT_CATEGORY_MAPPED_NOT_FOUND",
            )

        current = await self.repo.current_categories(product_id)

        to_add = list(set(category_ids) - current)
        to_remove = list(current - set(category_ids))

        await self.repo.add_links(product_id, to_add)
        await self.repo.remove_links(product_id, to_remove)
        await self.repo.commit()

        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("admin", "full", product_id)
            await self.cache.invalidate_key("user", "full", product_id)
            await self.cache.invalidate_key("user", product_id)
            await self.cache.invalidate_key("homepage")

        return ProductCategoryResult(
            product_id=product_id,
            attached=sorted(to_add),
            detached=sorted(to_remove),
            current=sorted(set(category_ids)),
        )
