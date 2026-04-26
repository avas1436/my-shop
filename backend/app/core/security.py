from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from fastapi import HTTPException
from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext
from redis.asyncio import Redis

from app.config.settings import get_settings

# =========================
# Password Hashing
# =========================
# ساخت هش
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


# ساخت پسورد هش شده برای ذخیره در دیتا بیس
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# مقایسه پسورد اصلی که کاربر میزند با چیزی که داخل دیتا بیس ذخیره شده بوده
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# =========================
# Refresh Session (Redis)
# =========================
def get_refresh_token_ttl() -> timedelta:
    return timedelta(days=settings.refresh_token_expire_days)


def build_refresh_token_key(token_id: str) -> str:
    return f"{settings.session_prefix}:refresh:{token_id}"


# ذخیره رفرش توکن داخل ردیس
async def store_refresh_token(
    redis_client: Redis | None,
    token_id: str,
    subject: str,
) -> None:
    if redis_client is None:
        return

    ttl = max(int(get_refresh_token_ttl().total_seconds()), 1)

    await redis_client.setex(build_refresh_token_key(token_id), ttl, subject)


# بررسی وجود رفرش توکن در ردیس
async def is_refresh_token_active(
    redis_client: Redis | None,
    token_id: str,
    subject: str,
) -> bool:

    if redis_client is None:
        return False

    stored_subject = await redis_client.get(build_refresh_token_key(token_id))

    return stored_subject == subject


# حذف رفرش توکن از ردیس
async def revoke_refresh_token(redis_client: Redis | None, token_id: str) -> None:
    if redis_client is None:
        return

    await redis_client.delete(build_refresh_token_key(token_id))


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
        "iat": now,  # Issued At
        "exp": expire,  # Expiration
        "jti": token_id,  # JWT ID
    }

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

    return create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_id=jti,
    )


# صحت و اعتبار یک توکن داده شده را بررسی میکند
def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])


# کاربردی تابع دیکد
def get_token_payload(token: str, expected_type: str = "access") -> dict[str, Any]:
    try:
        payload = decode_token(token=token)

    except JWTError as exc:
        raise ValueError("Invalid token") from exc

    exp = payload.get("exp")

    if exp and datetime.fromtimestamp(exp, tz=UTC) < datetime.now(UTC):
        raise HTTPException(
            status_code=401,
            detail="Token expired",
        )

    token_type = payload.get("type")
    subject = payload.get("sub")
    if token_type != expected_type or not subject:
        raise ValueError("Invalid token payload")

    return payload


def get_token_subject(token: str, expected_type: str = "access") -> str:
    payload = get_token_payload(token=token, expected_type=expected_type)
    return str(payload["sub"])
