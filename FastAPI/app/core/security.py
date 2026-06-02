# app/core/security.py
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext

from app.config.settings import get_settings
from app.errors.errors import Unauthorized

# =========================
# Config / Security setup
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


# =========================
# Password: hash & verify
# =========================
# ساخت پسورد هش شده برای ذخیره در دیتا بیس
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# مقایسه پسورد اصلی که کاربر میزند با چیزی که داخل دیتا بیس ذخیره شده بوده
def verify_password(password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(password, hashed_password)


# =========================
# JWT create / decode
# =========================
# با موارد دریافتی یک توکن میسازد
#  سابجکت اطلاعات کاربر مثلا شماره تلفن
#  تایپ تعیین کننده رفرش یا اکسس بودن
#  تاریخ انقضا هم داخل اطلاعات توکن است
# شناسه توکن هم برای حذف یا لیست سیاه کردن یک نشست بوسیله حذف رفرش توکن است
def create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    token_id: str | None = None,
) -> str:

    now = datetime.now(UTC)
    expire = now + expires_delta

    payload = {
        "sub": subject,  # Subject
        "token_type": token_type,  # "access" | "refresh"
        "iat": int(now.timestamp()),  # Issued At
        "exp": int(expire.timestamp()),  # Expiration
    }

    # jti فقط برای refresh لازم است
    if token_id is not None:
        payload["jti"] = token_id  # JWT ID

    return jwt.encode(
        claims=payload,
        key=settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )


# استفاده از تابع ساخت توکن برای ساخت اکسس توکن
def create_access_token(subject: str) -> str:

    return create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )


# برای ساخت رفرش توکن
def create_refresh_token(subject: str) -> str:
    jti = str(uuid4())
    token = create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_id=jti,
    )

    return token


# صحت و اعتبار یک توکن داده شده را بررسی میکند
def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return dict(payload)

    except JWTError as exc:
        raise Unauthorized(
            message="Invalid or expired token",
            code="INVALID_TOKEN",
        ) from exc


# =========================
# JWT validation helpers
# =========================
# اعتبار سنجی نوع توکن و اعتبار
def get_token_payload(token: str, expected_type: str = "access") -> dict[str, Any]:
    payload = decode_token(token=token)

    exp = payload.get("exp")

    if exp and datetime.fromtimestamp(exp, tz=UTC) < datetime.now(UTC):
        raise Unauthorized(
            message="Token has expired",
            code="TOKEN_EXPIRED",
        )

    token_type = payload.get("token_type")
    subject = payload.get("sub")

    if token_type != expected_type or not subject:
        raise Unauthorized(
            message="Invalid token payload",
            code="INVALID_TOKEN_PAYLOAD",
        )

    return payload


def get_token_subject(token: str, expected_type: str = "access") -> str:
    payload = get_token_payload(token=token, expected_type=expected_type)
    return str(payload["sub"])
