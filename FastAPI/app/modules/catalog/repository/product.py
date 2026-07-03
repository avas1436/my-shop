# app/modules/catalog/repository/product.py

from sqlalchemy import and_, case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from app.common.enums import ProductSortEnum
from app.modules.catalog.models.attribute import (
    Attribute,
    ProductAttribute,
    ProductVariantAttribute,
)
from app.modules.catalog.models.brand import Brand
from app.modules.catalog.models.category import Category
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.product_view import ProductAdminView
from app.modules.catalog.models.tag import Tag
from app.modules.catalog.models.variant import ProductVariant
from app.modules.catalog.schemas.product import (
    ProductAdminUpdate,
    ProductPublish,
    ProductSoftDelete,
)
from app.modules.comments.models import Comment


# =========================================================
# Product Repo for Admin
# =========================================================
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
    async def get_admin_product_view(
        self,
        product_id: int | None = None,
        slug: str | None = None,
        include_deleted: bool = False,
    ) -> ProductAdminView | None:

        stmt = select(ProductAdminView)

        if product_id is not None and slug is not None:
            raise ValueError("Provide either product_id or slug, not both")

        elif product_id is not None:
            stmt = stmt.where(ProductAdminView.id == product_id)

        elif slug is not None:
            stmt = stmt.where(ProductAdminView.slug == slug)

        else:
            return None

        # فیلتر کردن رکوردهای حذف شده در صورت نیاز
        if not include_deleted:
            stmt = stmt.where(ProductAdminView.deleted_at.is_(None))

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

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


# =========================================================
# Product Repo for User
# =========================================================
class UserProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------------------
    # Get Light Product by ID
    # ---------------------------------
    async def get_light_by_id(self, product_id: int) -> Product | None:
        stmt = (
            select(Product)
            .where(
                Product.id == product_id,
                Product.deleted_at.is_(None),
                Product.published_at.is_not(None),
            )
            .options(
                # در نمایش کارت معمولاً تصویر اصلی لازم است
                selectinload(Product.images),
                joinedload(Product.brand),
            )
        )
        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()

    # ---------------------------------
    # Get Light Product by Slug
    # ---------------------------------
    async def get_light_by_slug(self, slug: str) -> Product | None:
        stmt = (
            select(Product)
            .where(
                Product.slug == slug,
                Product.deleted_at.is_(None),
                Product.published_at.is_not(None),
            )
            .options(
                selectinload(Product.images),
                joinedload(Product.brand),
            )
        )
        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()

    # ---------------------------------
    # Get Full Product (detail page)
    # ---------------------------------
    async def get_full_product(
        self,
        product_id: int | None = None,
        slug: str | None = None,
    ) -> Product | None:

        if product_id is not None and slug is not None:
            raise ValueError("Provide either product_id or slug, not both")
        if product_id is None and slug is None:
            return None

        # --- subquery: last 5 comments per product ---
        comment_subq = select(
            Comment,
            func.row_number()
            .over(partition_by=Comment.product_id, order_by=Comment.created_at.desc())
            .label("rn"),
        ).subquery()

        # aliased comment
        CommentAlias = aliased(Comment, comment_subq)

        stmt = select(Product).outerjoin(
            CommentAlias,
            (Product.id == CommentAlias.product_id) & (comment_subq.c.rn <= 5),
        )

        if product_id is not None:
            stmt = stmt.where(Product.id == product_id)
        else:
            stmt = stmt.where(Product.slug == slug)

        stmt = stmt.where(
            Product.deleted_at.is_(None),
            Product.published_at.is_not(None),
        )

        stmt = stmt.options(
            joinedload(Product.brand),
            selectinload(Product.categories),
            selectinload(Product.tags),
            selectinload(Product.images),
            selectinload(Product.attribute_values).joinedload(
                ProductAttribute.attribute
            ),
            selectinload(Product.variants).options(
                joinedload(ProductVariant.inventory),
                selectinload(ProductVariant.attribute_values).joinedload(
                    ProductVariantAttribute.attribute
                ),
            ),
            # مهم: کامنت‌ها فقط از join محدود شده می‌آیند
            contains_eager(Product.comments, alias=CommentAlias),
        )

        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()

    # ---------------------------------
    # List products (Light) - paginated
    # ---------------------------------
    async def list_light_advanced(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        text: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        is_in_stock: bool | None = None,
        has_discount: bool | None = None,
        is_featured: bool | None = None,
        is_digital: bool | None = None,
        brand_slugs: list[str] | None = None,
        category_slugs: list[str] | None = None,
        tag_slugs: list[str] | None = None,
        # attribute_filters = { "color": ["red", "blue"], "size": ["xl"] }
        attribute_filters: dict[str, list[str]] | None = None,
        sort: ProductSortEnum = ProductSortEnum.NEWEST,
    ) -> list[Product]:

        stmt = select(Product).where(
            Product.deleted_at.is_(None),
            Product.published_at.is_not(None),
        )

        # ---- text search ----
        if text:
            stmt = stmt.where(
                or_(
                    Product.name.ilike(f"%{text}%"),
                    Product.slug.ilike(f"%{text}%"),
                    Product.description.ilike(f"%{text}%"),
                )
            )

        # ---- price range ----
        if min_price is not None:
            stmt = stmt.where(
                case(
                    (Product.discount_price.is_not(None), Product.discount_price),
                    else_=Product.price,
                )
                >= min_price
            )
        if max_price is not None:
            stmt = stmt.where(
                case(
                    (Product.discount_price.is_not(None), Product.discount_price),
                    else_=Product.price,
                )
                <= max_price
            )

        # ---- flags ----
        if is_in_stock is not None:
            stmt = stmt.where(Product.is_in_stock == is_in_stock)

        if has_discount is not None:
            if has_discount:
                stmt = stmt.where(Product.discount_price.is_not(None))
            else:
                stmt = stmt.where(Product.discount_price.is_(None))

        if is_featured is not None:
            stmt = stmt.where(Product.is_featured == is_featured)

        if is_digital is not None:
            stmt = stmt.where(Product.is_digital == is_digital)

        # ---- brands (by slug) ----
        if brand_slugs:
            stmt = stmt.join(Product.brand).where(Brand.slug.in_(brand_slugs))

        # ---- categories (by slug) ----
        if category_slugs:
            stmt = stmt.join(Product.categories).where(
                Category.slug.in_(category_slugs)
            )

        # ---- tags (by slug) ----
        if tag_slugs:
            stmt = stmt.join(Product.tags).where(Tag.slug.in_(tag_slugs))

        # ---- attributes (by slug) ----
        if attribute_filters:
            for attr_slug, values in attribute_filters.items():
                stmt = (
                    stmt.join(Product.attribute_values)  # ProductAttribute
                    .join(Attribute)
                    .where(
                        and_(
                            Attribute.slug == attr_slug,
                            ProductAttribute.value.in_(values),
                        )
                    )
                )

        # ---- sorting ----
        if sort == ProductSortEnum.PRICE_ASC:
            stmt = stmt.order_by(Product.final_price.asc())
        elif sort == ProductSortEnum.PRICE_DESC:
            stmt = stmt.order_by(Product.final_price.desc())
        elif sort == ProductSortEnum.DISCOUNT_DESC:
            stmt = stmt.order_by(Product.discount_percent.desc())
        else:
            stmt = stmt.order_by(Product.published_at.desc())

        stmt = stmt.distinct()

        # ---- count ----
        count_query = select(func.count()).select_from(stmt.subquery())

        total = (await self.db.execute(count_query)).scalar_one()

        # ---- paging + load ----
        stmt = (
            stmt.options(
                selectinload(Product.images),
                joinedload(Product.brand),
            )
            .offset(offset)
            .limit(limit)
        )

        items = (await self.db.execute(stmt)).scalars().all()
        return list(items), total

    async def get_homepage_featured(
        self,
        *,
        limit: int = 12,
        order_by_discount: bool = True,
        order_by_newest: bool = True,
    ) -> list[Product]:
        stmt = select(Product).where(
            Product.deleted_at.is_(None),
            Product.published_at.is_not(None),
            Product.is_featured.is_(True),
        )

        if order_by_discount:
            stmt = stmt.order_by(Product.discount_percent.desc())
        if order_by_newest:
            stmt = stmt.order_by(Product.published_at.desc())

        stmt = stmt.limit(limit).options(
            selectinload(Product.images),
            joinedload(Product.brand),
        )

        items = (await self.db.execute(stmt)).scalars().all()
        return list(items)
