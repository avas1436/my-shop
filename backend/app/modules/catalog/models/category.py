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

# from app.modules.catalog.models.product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str | None] = mapped_column(String(120), nullable=True)

    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    parent: Mapped[Category | None] = relationship(
        remote_side="Category.id", back_populates="children"
    )
    children: Mapped[list[Category]] = relationship(back_populates="parent")

    products: Mapped[list[Product]] = relationship(
        secondary="product_categories", back_populates="categories"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    __table_args__ = (
        Index(
            "idx_unique_category_slug_not_null",
            "slug",
            unique=True,
            postgresql_where=text("slug is not null"),
        ),
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class ProductCategory(Base):
    __tablename__ = "product_categories"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )

    __table_args__ = (
        UniqueConstraint("product_id", "category_id", name="uq_product_category"),
    )
