from __future__ import annotations

from datetime import datetime

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
from app.modules.catalog.models.product import Product


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str | None] = mapped_column(String(120), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    products: Mapped[list[Product]] = relationship(
        secondary="product_tags", back_populates="tags"
    )

    __table_args__ = (
        Index(
            "idx_unique_tag_slug_not_null",
            "slug",
            unique=True,
            postgresql_where=text("slug is not null"),
        ),
    )


class ProductTag(Base):
    __tablename__ = "product_tags"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)

    __table_args__ = (UniqueConstraint("product_id", "tag_id", name="uq_product_tag"),)
