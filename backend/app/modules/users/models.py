from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Date, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.common.enums import UserRole
from app.core.database import Base


# ==============================================================================
# User Model
# ==============================================================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    first_name: Mapped[Optional[str]] = mapped_column(
        String(50), default=None, nullable=False
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(50), default=None, nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )
    is_phone_verified = mapped_column(Boolean, default=False)

    birth_date: Mapped[Optional[date]] = mapped_column(Date)

    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="UserRole"), default=UserRole.CUSTOMER, nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
