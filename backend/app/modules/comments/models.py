# app/modules/comments/models.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    rating: Mapped[int] = mapped_column(
        Integer, CheckConstraint("rating BETWEEN 1 AND 5"), default=5
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_name: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    product = relationship("Product", back_populates="comments")
    user = relationship("User", back_populates="comments")

    __table_args__ = (Index("idx_comment_product_id", "product_id"),)
