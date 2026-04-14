from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_token_subject


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        subject = get_token_subject(token, expected_type="access")
        return int(subject)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
