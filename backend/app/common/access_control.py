from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from datetime import UTC, datetime, timedelta
from typing import Annotated

from backend.app.core.jwt import get_current_user
from fastapi import Depends, HTTPException, Request

from app.common.enums import UserRole
from app.modules.users.models import User

# -----------------------------
# Type aliases
# -----------------------------
UserCheck = Callable[[User, Request], None]  # custom check function


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _forbidden(detail: str) -> None:
    raise HTTPException(
        status_code=403,
        detail=detail,
    )


def require_access(
    allowed_roles: Iterable[UserRole],
    *,
    # پایه
    require_active: bool = True,
    require_not_deleted: bool = True,
    require_phone_verified: bool = True,
    # (1) ورود اخیر
    require_recent_login_within: timedelta | None = None,
    # (2) داشتن رمز عبور
    require_password: bool = False,
    # (3) تکمیل پروفایل
    require_profile_complete: bool = False,
    profile_required_fields: Sequence[str] = ("first_name", "last_name"),
    # (5) deny roles
    deny_roles: Iterable[UserRole] | None = None,
):
    """
    Advanced authz dependency factory for FastAPI routes.
    """
    allowed_roles = set(allowed_roles)
    deny_roles = set(deny_roles or [])

    async def role_checker(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        now = _utcnow()

        # پایه: حذف/فعال/تایید موبایل
        if (
            require_not_deleted
            and getattr(current_user, "deleted_at", None) is not None
        ):
            _forbidden("deleted user")

        if require_active and not bool(getattr(current_user, "is_active", False)):
            _forbidden("inactive user")

        if require_phone_verified and not bool(
            getattr(current_user, "is_phone_verified", False)
        ):
            _forbidden("phone not verified")

        # (5) deny roles اول بررسی شود
        if getattr(current_user, "role", None) in deny_roles:
            _forbidden("role is explicitly denied")

        # نقش مجاز
        if getattr(current_user, "role", None) not in allowed_roles:
            _forbidden("access denied")

        # (1) ورود اخیر
        if require_recent_login_within is not None:
            last_login = getattr(current_user, "last_login", None)

            if last_login is None:
                _forbidden("recent login required")

            assert isinstance(last_login, datetime)

            # normalize tz
            if last_login.tzinfo is None:
                last_login = last_login.replace(tzinfo=UTC)

            if now - last_login > require_recent_login_within:
                _forbidden("session too old, re-authentication required")

        # (2) داشتن رمز
        if require_password:
            hp = getattr(current_user, "hashed_password", None)
            if not hp or not str(hp).strip():
                _forbidden("password is required for this action")

        # (3) پروفایل کامل
        if require_profile_complete:
            missing = []
            for field in profile_required_fields:
                val = getattr(current_user, field, None)
                if val is None or (isinstance(val, str) and not val.strip()):
                    missing.append(field)
            if missing:
                _forbidden(f"profile incomplete: missing {', '.join(missing)}")

        return current_user

    return role_checker


# -----------------------------
# How To Use
# -----------------------------

# # پایه
# require_roles([UserRole.ADMIN])

# # این سه مورد پیش فرض فعالند
# require_active = True
# require_not_deleted = True
# require_phone_verified = True

# # عملیات حساس؛ اگر login قدیمی بود، re-login لازم شود.
# equire_recent_login_within = timedelta(minutes=15)

# # کاربرانی که فقط با او تی پی وارد می‌شوند را برای عملیات خاص محدود کنید.
# require_password = True

# #  اجبار به تکمیل پروفایل
# require_profile_complete = True
# profile_required_fields = ("first_name", "last_name", "birth_date")

# # حتی اگر در allow بود، deny همیشه غالب باشد.
# deny_roles = [UserRole.BANNED]
