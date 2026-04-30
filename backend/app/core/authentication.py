# app/core/authentication.py
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_token_payload

# طبق منطق این فایل تنها باید ارور 401 خروجی بدهد و 403 مربوط
# به قسمتی است که بررسی می کند چه کسی اجازه ورود دارد
from app.errors.errors import Unauthorized  # HTTPError 401
from app.modules.users.models import User
from app.modules.users.repository import UserRepository

# auto_error=False => خودمان خطای استانداردتر بدهیم
bearer_scheme = HTTPBearer(auto_error=False)  # JWT


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:

    if credentials is None or not credentials.credentials:
        raise Unauthorized("Not authenticated")

    token = credentials.credentials

    # expected_type="access" را enforce می‌کند
    payload = get_token_payload(token=token, expected_type="access")

    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject.strip():
        raise Unauthorized("Invalid token payload")

    repo = UserRepository(db)

    user = await repo.get_by_phone(subject)

    if user is None:
        raise Unauthorized("User not found")

    # وضعیت پایه کاربر
    if not user.is_active:
        raise Unauthorized("Inactive user")

    if user.deleted_at is not None:
        raise Unauthorized("Deleted user")

    return user
