from __future__ import annotations

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.modules.catalog.models.product import Product


class ProductImage(Base):
    __tablename__ = "product_images"

    __table_args__ = (
        Index(
            "idx_unique_primary_image",
            "product_id",
            unique=True,
            postgresql_where=text("is_primary = true"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    alt_text: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="توضیح عکس برای سئو و دسترسی"
    )
    is_primary: Mapped[bool] = mapped_column(
        default=False, comment="آیا این عکس تصویر اصلی محصول است"
    )
    sort_order: Mapped[int] = mapped_column(default=0, comment="ترتیب نمایش عکس‌ها")

    product: Mapped[Product] = relationship(back_populates="images")
