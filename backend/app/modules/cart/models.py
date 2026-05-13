# app/modules/cart/models.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import CartStatus
from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.catalog.models.variant import ProductVariant


# ---------------------------
# Cart
# ---------------------------
class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    status: Mapped[CartStatus] = mapped_column(
        Enum(CartStatus, name="cart_status"),
        default=CartStatus.ACTIVE,
        nullable=False,
        index=True,
    )

    total_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    discount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    items: Mapped[list[CartItem]] = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )

    __table_args__ = (Index("idx_carts_user_id", "user_id"),)


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"),
        nullable=False,
    )
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variants.id", ondelete="CASCADE"),
        nullable=False,
    )

    qty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    cart: Mapped[Cart] = relationship(
        "Cart",
        back_populates="items",
    )

    variant: Mapped[ProductVariant] = relationship("ProductVariant")

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "variant_id",
            name="uq_cart_items_cart_variant",
        ),
        Index(
            "idx_cart_items_cart_id_variant_id",
            "cart_id",
            "variant_id",
        ),
    )
