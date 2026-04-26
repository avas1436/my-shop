from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.catalog.models.attribute import ProductVariantAttribute
    from app.modules.catalog.models.product import Product


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # اگر خالی باشد از قیمت محصول استفاده می‌شود
    price: Mapped[int | None] = mapped_column(
        Integer, comment="قیمت خاص واریانت (واحد کوچک پول)"
    )

    is_active: Mapped[bool] = mapped_column(default=True)

    product: Mapped[Product] = relationship(back_populates="variants")

    attribute_values: Mapped[list[ProductVariantAttribute]] = relationship(
        back_populates="variant", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "price IS NULL OR price >= 0", name="ck_variant_price_non_negative"
        ),
    )

    @property
    def final_price(self) -> int:
        return self.product.calculate_final_price(self.price)
