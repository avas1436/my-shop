# app/modules/catalog/models/product_view.py
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base

# ۱. نگهداری سورس SQL برای Alembic
CREATE_PRODUCT_ADMIN_VIEW_SQL = """
-- =========================================================
-- product_admin_view
-- =========================================================

CREATE OR REPLACE VIEW product_admin_view AS
SELECT
    p.id,
    p.name,
    p.slug,
    p.sku,
    p.description,
    p.price,
    p.discount_price,
    p.cost_price,
    p.tax_rate,

    -- discount_percent: hybrid_property، ستون واقعی نیست
    CASE
        WHEN p.discount_price IS NOT NULL AND p.price > 0
        THEN ROUND((1 - p.discount_price::numeric / p.price::numeric) * 100, 1)
        ELSE 0.0
    END AS discount_percent,

    -- final_price: معادل Product.calculate_final_price() با base_price=None => bp=price
    CASE
        WHEN p.discount_price IS NOT NULL
             AND p.price > 0
             AND p.discount_price <= p.price
        THEN GREATEST(p.discount_price, 0)
        ELSE p.price
    END AS final_price,

    -- price_with_tax: int(final_price * (1 + tax_rate/10000)) => FLOOR برای اعداد مثبت
    FLOOR(
        (CASE
            WHEN p.discount_price IS NOT NULL
                 AND p.price > 0
                 AND p.discount_price <= p.price
            THEN GREATEST(p.discount_price, 0)
            ELSE p.price
        END)::numeric
        * (1 + p.tax_rate::numeric / 10000)
    )::int AS price_with_tax,

    COALESCE(inv_agg.total_available_quantity, 0) AS total_available_quantity,

    -- is_in_stock سطح محصول: any(variant.inventory.is_in_stock) که خودش
    -- available_quantity>0 OR allow_backorder است (نه فقط total>0)
    COALESCE(inv_agg.any_in_stock, false) AS is_in_stock,

    p.currency_code,
    p.status,
    p.is_featured,
    p.is_digital,
    p.weight,
    p.width,
    p.height,
    p.depth,
    p.meta_title,
    p.meta_description,
    p.gtin,
    p.created_at,
    p.updated_at,
    p.published_at,
    p.deleted_at,

    -- برند
    CASE
        WHEN b.id IS NULL THEN NULL
        ELSE json_build_object(
            'id', b.id,
            'name', b.name,
            'slug', b.slug,
            'created_at', b.created_at,
            'updated_at', b.updated_at
        )
    END AS brand,

    COALESCE(cat_agg.categories, '[]'::json) AS categories,
    COALESCE(tag_agg.tags, '[]'::json) AS tags,
    COALESCE(img_agg.images, '[]'::json) AS images,
    COALESCE(inv_agg.inventory, '[]'::json) AS inventory,
    COALESCE(attr_agg.attributes, '[]'::json) AS attributes

FROM products p

-- برند
LEFT JOIN brands b ON b.id = p.brand_id

-- دسته‌بندی‌ها
LEFT JOIN LATERAL (
    SELECT json_agg(
        json_build_object(
            'id', c.id,
            'name', c.name,
            'slug', c.slug,
            'description', c.description,
            'is_active', c.is_active,
            'parent_id', c.parent_id,
            'created_at', c.created_at,
            'updated_at', c.updated_at
        )
    ) AS categories
    FROM categories c
    JOIN product_categories pc ON pc.category_id = c.id
    WHERE pc.product_id = p.id
) cat_agg ON true

-- تگ‌ها
LEFT JOIN LATERAL (
    SELECT json_agg(
        json_build_object(
            'id', t.id,
            'name', t.name,
            'slug', t.slug,
            'created_at', t.created_at
        )
    ) AS tags
    FROM tags t
    JOIN product_tags pt ON pt.tag_id = t.id
    WHERE pt.product_id = p.id
) tag_agg ON true

-- تصاویر
LEFT JOIN LATERAL (
    SELECT json_agg(
        json_build_object(
            'id', pic.id,
            'product_id', pic.product_id,
            'url', pic.url,
            'alt_text', pic.alt_text,
            'is_primary', pic.is_primary,
            'sort_order', pic.sort_order
        )
        ORDER BY pic.sort_order
    ) AS images
    FROM product_images pic
    WHERE pic.product_id = p.id
) img_agg ON true

-- ویژگی‌های سطح محصول
LEFT JOIN LATERAL (
    SELECT json_agg(
        json_build_object(
            'attribute_id', attr.id,
            'name', attr.name,
            'value', pattr.value,
            'scope', 'product'
        )
    ) AS attributes
    FROM attributes attr
    JOIN product_attributes pattr ON pattr.attribute_id = attr.id
    WHERE pattr.product_id = p.id
) attr_agg ON true

-- موجودی‌
LEFT JOIN LATERAL (
    SELECT
        json_agg(inv_row.inv_obj) AS inventory,
        COALESCE(SUM(inv_row.available_quantity), 0) AS total_available_quantity,
        BOOL_OR(inv_row.item_is_in_stock) AS any_in_stock
    FROM (
        SELECT
            json_build_object(
                'id', inv.id,
                'variant_id', var.id,
                'sku', var.sku,
                'price', var.price,
                'final_price', GREATEST(
                    (CASE
                        WHEN p.discount_price IS NOT NULL
                             AND p.price > 0
                             AND p.discount_price <= p.price
                        THEN ROUND(
                            COALESCE(var.price, p.price)::numeric
                            * p.discount_price::numeric / p.price::numeric
                        )
                        ELSE COALESCE(var.price, p.price)::numeric
                    END)::int,
                    0
                ),
                'is_active', var.is_active,
                'quantity', inv.quantity,
                'reserved_quantity', inv.reserved_quantity,
                'low_stock_alert', inv.low_stock_alert,
                'allow_backorder', inv.allow_backorder,
                'updated_at', inv.updated_at,
                'available_quantity', GREATEST(inv.quantity - inv.reserved_quantity, 0),
                'is_in_stock', (GREATEST(inv.quantity - inv.reserved_quantity, 0) > 0)
                               OR inv.allow_backorder,
                'attributes', COALESCE(
                    (
                        SELECT json_agg(
                            json_build_object(
                                'attribute_id', atr.id,
                                'name', atr.name,
                                'value', pva.value,
                                'scope', 'variant',
                                'variant_id', pva.variant_id
                            )
                        )
                        FROM product_variant_attributes pva
                        JOIN attributes atr ON atr.id = pva.attribute_id
                        WHERE pva.variant_id = var.id
                    ),
                    '[]'::json
                )
            ) AS inv_obj,
            GREATEST(inv.quantity - inv.reserved_quantity, 0) AS available_quantity,
            (GREATEST(inv.quantity - inv.reserved_quantity, 0) > 0)
                OR inv.allow_backorder AS item_is_in_stock
        FROM product_variants var
        JOIN inventories inv ON inv.variant_id = var.id
        WHERE var.product_id = p.id
    ) inv_row
) inv_agg ON true;
"""

DROP_PRODUCT_ADMIN_VIEW_SQL = "DROP VIEW IF EXISTS product_admin_view;"


# ۲. ساخت مدل SQLAlchemy برای کوئری زدن در پایتون
class ProductAdminView(Base):
    __tablename__ = "product_admin_view"

    # این تنظیمات به SQLAlchemy می‌گوید که این یک جدول معمولی نیست و نباید سعی کند آن را بسازد
    __table_args__ = {"info": {"is_view": True}}

    # فیلدهای پایه
    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    sku = Column(String)
    description = Column(Text)

    # فیلدهای مالی
    price = Column(Integer)
    discount_price = Column(Integer)
    cost_price = Column(Integer)
    tax_rate = Column(Integer)
    discount_percent = Column(Float)
    final_price = Column(Integer)
    price_with_tax = Column(Integer)

    # وضعیت و موجودی
    total_available_quantity = Column(Integer)
    is_in_stock = Column(Boolean)
    currency_code = Column(String)
    status = Column(String)
    is_featured = Column(Boolean)
    is_digital = Column(Boolean)

    # ابعاد فیزیکی
    weight = Column(Numeric(precision=10, scale=3))
    width = Column(Numeric(precision=10, scale=2))
    height = Column(Numeric(precision=10, scale=2))
    depth = Column(Numeric(precision=10, scale=2))

    # سئو و شناسه بین‌المللی
    meta_title = Column(String)
    meta_description = Column(Text)
    gtin = Column(String)

    # تاریخ‌ها
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))

    # روابط (تجمیع شده به صورت JSON)
    brand = Column(JSONB)
    categories = Column(JSONB)
    tags = Column(JSONB)
    images = Column(JSONB)
    inventory = Column(JSONB)
    attributes = Column(JSONB)
