from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.catalog.models.product import Product


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True)

    quantity: Mapped[int] = mapped_column(default=0)
    reserved_quantity: Mapped[int] = mapped_column(default=0)
    low_stock_alert: Mapped[int] = mapped_column(default=5)
    allow_backorder: Mapped[bool] = mapped_column(
        default=False,
        comment="آیا فروش بدون موجودی مجاز است یا خیر",
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    product: Mapped[Product] = relationship(back_populates="inventory")

    __table_args__ = (
        CheckConstraint(
            "(product_id IS NOT NULL AND variant_id IS NULL) OR "
            "(product_id IS NULL AND variant_id IS NOT NULL)",
            name="ck_inventory_product_or_variant",
        ),
        CheckConstraint("quantity >= 0", name="ck_inventory_quantity_non_negative"),
        CheckConstraint(
            "reserved_quantity >= 0",
            name="ck_inventory_reserved_non_negative",
        ),
    )

    @property
    def available_quantity(self) -> int:
        return max(0, self.quantity - self.reserved_quantity)

    @property
    def is_in_stock(self) -> bool:
        return self.available_quantity > 0 or self.allow_backorder
