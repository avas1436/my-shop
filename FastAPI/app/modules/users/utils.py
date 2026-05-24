# app/modules/users/utils.py
import re

from fastapi import Cookie, Response

from app.cache.cache import RedisCache
from app.config.settings import get_settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_token_payload,
)
from app.errors.errors import Unauthorized
from app.modules.users.models import User

settings = get_settings()


# ==============================================================================
# Phone Number Validator
# ==============================================================================
def validate_phone(phone_number: str):
    if phone_number is None:
        return phone_number

    # تبدیل اعداد فارسی
    persian = "۰۱۲۳۴۵۶۷۸۹"
    english = "0123456789"
    table = str.maketrans(persian, english)
    phone_number = phone_number.translate(table)

    # حذف کاراکترهای غیر عدد
    phone_number = re.sub(r"\D", "", phone_number)

    # normalize
    if phone_number.startswith("989"):
        phone_number = "0" + phone_number[2:]
    elif phone_number.startswith("98"):
        phone_number = "0" + phone_number[2:]
    elif phone_number.startswith("9") and len(phone_number) == 10:
        phone_number = "0" + phone_number

    if not re.fullmatch(r"09\d{9}", phone_number):
        raise ValueError("Phone number must be a valid Iranian mobile number")

    return phone_number


# ==============================================================================
# Password Validator
# ==============================================================================
def validate_password(password: str):

    # if not any(c.isupper() for c in password):
    #     raise ValueError("Password must contain uppercase")

    # if not any(c.islower() for c in password):
    #     raise ValueError("Password must contain lowercase")

    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain digit")

    # if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
    #     raise ValueError("Password must contain special char")


# ==============================================================================
# Token Maker
# ==============================================================================
async def issue_access_token(user: User) -> str:
    access_token = create_access_token(subject=user.phone_number)

    return access_token


async def issue_refresh_token(user: User, cache: RedisCache) -> str:
    refresh_token = create_refresh_token(subject=user.phone_number)
    refresh_payload = get_token_payload(refresh_token, expected_type="refresh")

    await cache.store(
        jti=str(refresh_payload["jti"]),
        subject=str(refresh_payload["sub"]),
    )

    return refresh_token


# ====================================================================
# Helper Function for Setting Cookie
# ====================================================================
def set_refresh_token_cookie(
    response: Response,
    refresh_token: str,
):

    age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # در پروداکشن که HTTPS است حتماً True باشد
        samesite="lax",  # یا "strict"
        max_age=age,
    )


def delete_refresh_token_cookie(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )


def get_refresh_token(refresh_token: str | None = Cookie(None)) -> str:
    if not refresh_token:
        raise Unauthorized("Missing refresh token")
    return refresh_token
