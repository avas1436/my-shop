from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_token_subject
from app.modules.users.models import User
from app.modules.users.repository import UserRepository

# from app.crud import users

bearer_scheme = HTTPBearer()  # JWT


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:

    phone = get_token_subject(token.credentials)

    if not phone:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    user = await UserRepository.get_by_phone(db=db, phone_number=phone)

    if not user or not user.is_active or user.deleted_at is not None:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive",
        )

    return user
