from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.common.enums import UserRole
from app.core.jwt import get_current_user
from app.modules.users.models import User


async def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:

    if (
        current_user.role != UserRole.ADMIN
        and current_user.is_active
        and not current_user.deleted_at
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only admin",
        )
    return current_user
