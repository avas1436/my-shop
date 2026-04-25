from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class UserRepository:
    # @staticmethod
    # async def create(db: AsyncSession, user: User) -> User:
    #     db.add(user)
    #     await db.commit()
    #     await db.refresh(user)
    #     return user

    # @staticmethod
    # async def get_by_email(email: str) -> User | None:
    #     result = await db.execute(select(User).where(User.email == email))
    #     return result.scalar_one_or_none()

    # @staticmethod
    # async def get_by_id(user_id: int) -> User | None:
    #     result = await db.execute(select(User).where(User.id == user_id))
    #     return result.scalar_one_or_none()

    @staticmethod
    async def get_by_phone(db: AsyncSession, phone_number: str) -> User | None:
        stmt = select(User).where(User.phone_number == phone_number)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()
