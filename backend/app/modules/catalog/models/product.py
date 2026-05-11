# app/modules/catalog/models/product.py
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    case,
    func,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import ProductStatus
from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.catalog.models.attribute import ProductAttribute
    from app.modules.catalog.models.brand import Brand
    from app.modules.catalog.models.category import Category
    from app.modules.catalog.models.image import ProductImage
    from app.modules.catalog.models.tag import Tag
    from app.modules.catalog.models.variant import ProductVariant


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, comment="شناسه محصول و یک کد یکتاست"
    )
    sku: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="کد یکتای کالا در سیستم انبار داری",
    )
    slug: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="رشته مناسب آدرس سایت (برای فروشگاه حضوری می‌تواند خالی باشد)",
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="نام کالا")
    description: Mapped[str | None] = mapped_column(
        Text, comment="توضیح کامل همراه با HTML"
    )

    # قیمت‌ها به صورت عدد صحیح (واحد پول کوچک مثل ریال/تومان بدون اعشار)
    price: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="قیمت پایه کالا (واحد کوچک پول)"
    )
    discount_price: Mapped[int | None] = mapped_column(
        Integer, comment="قیمت تخفیفی کالا (واحد کوچک پول)"
    )
    cost_price: Mapped[int | None] = mapped_column(
        Integer, comment="قیمت خرید کالا (محرمانه)"
    )

    # مالیات و واحد پول
    tax_rate: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="نرخ مالیات به واحد صدم درصد (basis points). مثال: 900=9.00%",
    )
    currency_code: Mapped[str] = mapped_column(
        String(3), default="IRR", comment="کد ارز (مثلاً IRR)"
    )

    status: Mapped[ProductStatus] = mapped_column(
        Enum(ProductStatus),
        default=ProductStatus.DRAFT,
        comment="وضعیت محصول",
    )
    is_featured: Mapped[bool] = mapped_column(
        default=False, comment="آیا کالا شاخص است"
    )
    is_digital: Mapped[bool] = mapped_column(
        default=False, comment="آیا کالا دیجیتال قابل دانلود است"
    )

    # ابعاد و وزن
    weight: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    width: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    height: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    depth: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))

    # سئو
    meta_title: Mapped[str | None] = mapped_column(String(255))
    meta_description: Mapped[str | None] = mapped_column(String(500))

    # GTIN / Barcode
    gtin: Mapped[str | None] = mapped_column(
        String(20), unique=True, comment="شناسه جهانی کالا (GTIN/EAN/UPC)"
    )

    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # روابط
    brand: Mapped[Brand | None] = relationship(back_populates="products")
    categories: Mapped[list[Category]] = relationship(
        secondary="product_categories", back_populates="products"
    )

    tags: Mapped[list[Tag]] = relationship(
        secondary="product_tags", back_populates="products"
    )

    images: Mapped[list[ProductImage]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    # inventory: Mapped[Inventory | None] = relationship(
    #     back_populates="product", uselist=False, cascade="all, delete-orphan"
    # )

    variants: Mapped[list[ProductVariant]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    attribute_values: Mapped[list[ProductAttribute]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        # قیود قیمتی
        CheckConstraint("price >= 0", name="ck_product_price_non_negative"),
        CheckConstraint(
            "discount_price IS NULL OR discount_price >= 0",
            name="ck_product_discount_non_negative",
        ),
        CheckConstraint(
            "cost_price IS NULL OR cost_price >= 0",
            name="ck_product_cost_non_negative",
        ),
        CheckConstraint(
            "discount_price IS NULL OR discount_price <= price",
            name="ck_product_discount_le_price",
        ),
        # slug یکتا فقط زمانی که مقدار دارد
        Index(
            "idx_unique_product_slug_not_null",
            "slug",
            unique=True,
            postgresql_where=text("slug is not null"),
        ),
        Index("idx_product_name", "name"),  # برای جستجوی نام
        Index("idx_product_status", "status"),  # فیلتر بر اساس وضعیت
        Index("idx_product_created", "created_at"),  # مرتب‌سازی تاریخ
        Index("idx_product_price", "price"),  # مرتب‌سازی قیمت
        Index("idx_product_brand_id", "brand_id"),  # سرچ برند
        Index("idx_product_published_at", "published_at"),  # جستجوی زمان انتشار
        Index(
            "idx_product_featured_active",
            "published_at",
            postgresql_where=text(
                "is_featured = true AND status = 'ACTIVE' AND deleted_at IS NULL"
            ),  # فیلتر های پرتکرار برای لیست کاربران
        ),
        Index(
            "idx_product_status_deleted_created", "status", "deleted_at", "created_at"
        ),  # سرچ های مورد نیاز برای جستجوی صفحه اصلی
    )

    # فیلترهای پرتکرار (لیست عمومی)

    # صفحه اصلی: featured فقط محصولات فعال و حذف نشده

    def calculate_final_price(self, base_price: int | None = None) -> int:
        """
        اگر base_price داده شود (مثلاً قیمت واریانت)،
        تخفیف درصدی محصول روی آن اعمال می‌شود.
        """
        bp = base_price if base_price is not None else self.price
        if (
            self.discount_price is not None
            and self.price > 0
            and self.discount_price <= self.price
        ):
            # محاسبه درصد تخفیف از روی قیمت محصول
            discount_percent = 1 - (self.discount_price / self.price)
            final = int(round(bp * (1 - discount_percent)))
            return max(final, 0)
        return bp

    @property
    def final_price(self) -> int:
        return self.calculate_final_price()

    # محاسبه قیمت با مالیات
    @property
    def price_with_tax(self) -> int:
        return int(self.final_price * (1 + self.tax_rate / 10000))

    @hybrid_property
    def discount_percent(self) -> float:
        if self.discount_price is not None and self.price > 0:
            return float(round((1 - self.discount_price / self.price) * 100, 1))
        return 0.0

    @discount_percent.expression
    def discount_percent_expr(cls):
        return case(
            (
                (cls.discount_price.is_not(None)) & (cls.price > 0),
                func.round(
                    (1 - (cls.discount_price / cls.price)) * 100,
                    1,
                ),
            ),
            else_=0.0,
        )

    @property
    def total_available_quantity(self) -> int:
        return sum(
            (v.inventory.available_quantity if v.inventory else 0)
            for v in self.variants
        )

    @property
    def is_in_stock(self) -> bool:
        return any(
            (v.inventory.is_in_stock if v.inventory else False) for v in self.variants
        )

    # @property
    # def product_attributes(self):
    #     return self.attribute_values

    # @property
    # def variant_attributes(self):
    #     return [av for v in self.variants for av in v.attribute_values]

    @property
    def inventory(self):
        # مپ کردن attributeها بر اساس variant_id
        attrs_map = {}
        for v in self.variants:
            attrs_map[v.id] = [
                {
                    "attribute_id": va.attribute_id,
                    "name": va.attribute.name if va.attribute else None,
                    "value": va.value,
                    "scope": "variant",
                    "variant_id": v.id,
                }
                for va in v.attribute_values
            ]

        items = []
        for v in self.variants:
            inv = v.inventory
            if not inv:
                continue

            items.append(
                {
                    "id": inv.id,
                    "variant_id": v.id,
                    "sku": v.sku,
                    "price": v.price,
                    "final_price": v.final_price,
                    "is_active": v.is_active,
                    "quantity": inv.quantity,
                    "reserved_quantity": inv.reserved_quantity,
                    "low_stock_alert": inv.low_stock_alert,
                    "allow_backorder": inv.allow_backorder,
                    "updated_at": inv.updated_at,
                    "available_quantity": inv.available_quantity,
                    "is_in_stock": inv.is_in_stock,
                    "attributes": attrs_map.get(v.id, []),  # ✅ الحاق
                }
            )
        return items

    # پراپرتی آدرس محصول
    # @property
    # def url(self) -> str | None:
    #     if self.slug:
    #         return f"/products/{self.slug}"
    #     return f"/products/{self.id}"

    @property
    def attributes(self):
        return [
            {
                "attribute_id": pa.attribute_id,
                "name": pa.attribute.name if pa.attribute else None,
                "value": pa.value,
                "scope": "product",
            }
            for pa in self.attribute_values
        ]  # + [
        #     {
        #         "attribute_id": va.attribute_id,
        #         "name": va.attribute.name if va.attribute else None,
        #         "value": va.value,
        #         "scope": "variant",
        #         "variant_id": va.variant_id,
        #     }
        #     for v in self.variants
        #     for va in v.attribute_values
        # ]

    def __repr__(self) -> str:
        return f"<Product {self.name} | SKU: {self.sku}>"
