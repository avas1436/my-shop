# app/modules/catalog/models/attribute.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.catalog.models.product import Product
    from app.modules.catalog.models.variant import ProductVariant


# --------------------------------------------------
# Attribure Model
# --------------------------------------------------
class Attribute(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    slug: Mapped[str | None] = mapped_column(String(150), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        Index(
            "idx_unique_attribute_slug_not_null",
            "slug",
            unique=True,
            postgresql_where=text("slug is not null"),
        ),
    )


# --------------------------------------------------
# Product Attribure Model
# --------------------------------------------------
class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"), index=True)

    value: Mapped[str] = mapped_column(String(255), nullable=False)

    product: Mapped[Product] = relationship(back_populates="attribute_values")
    attribute: Mapped[Attribute] = relationship()

    __table_args__ = (
        UniqueConstraint("product_id", "attribute_id", name="uq_product_attribute"),
        Index("idx_product_attribute_attr_value", "attribute_id", "value"),
    )


# --------------------------------------------------
# Product Variant Attribure Model
# --------------------------------------------------
class ProductVariantAttribute(Base):
    __tablename__ = "product_variant_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variants.id"), index=True
    )
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"), index=True)
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    variant: Mapped[ProductVariant] = relationship(back_populates="attribute_values")
    attribute: Mapped[Attribute] = relationship()

    __table_args__ = (
        UniqueConstraint("variant_id", "attribute_id", name="uq_variant_attribute"),
    )
