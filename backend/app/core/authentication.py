from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_token_payload
from app.modules.users.models import User
from app.modules.users.repository import UserRepository

# auto_error=False => خودمان خطای استانداردتر بدهیم
bearer_scheme = HTTPBearer(auto_error=False)  # JWT


def _unauthorized(detail: str = "Could not validate credentials") -> HTTPException:

    return HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:

    if credentials is None or not credentials.credentials:
        raise _unauthorized("Not authenticated")

    token = credentials.credentials

    # expected_type="access" را enforce می‌کند
    payload = get_token_payload(token=token, expected_type="access")

    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject.strip():
        raise _unauthorized("Invalid token payload")

    repo = UserRepository(db)

    user = await repo.get_by_phone(subject)

    if user is None:
        raise _unauthorized("User not found")

    # وضعیت پایه کاربر
    if not user.is_active:
        raise _unauthorized("Inactive user")

    if user.deleted_at is not None:
        raise _unauthorized("Deleted user")

    return user
