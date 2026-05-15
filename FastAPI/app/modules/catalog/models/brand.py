# app/modules/catalog/models/brand.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.catalog.models.product import Product


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    slug: Mapped[str | None] = mapped_column(String(180), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    products: Mapped[list[Product]] = relationship(back_populates="brand")

    __table_args__ = (
        Index(
            "idx_unique_brand_slug_not_null",
            "slug",
            unique=True,
            postgresql_where=text("slug is not null"),
        ),
    )

    def __repr__(self) -> str:
        return f"<Brand {self.name}>"
