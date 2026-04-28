from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------------
    # Read
    # ---------------------------
    async def get_by_phone(self, phone_number: str) -> User | None:
        stmt = select(User).where(User.phone_number == phone_number).limit(1)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id).limit(1)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    # ---------------------------
    # Create
    # ---------------------------
    async def create_user(self, phone_number: str) -> User:
        user = User(phone_number=phone_number, is_verified=True)
        self.db.add(user)
        await self.db.flush()  # برای گرفتن id بدون commit
        return user

    def mark_verified(self, user: User) -> bool:
        changed = False
        if not user.is_verified:
            user.is_verified = True
            changed = True
        return changed

    def update_login(self, user: User) -> bool:

        user.last_login = datetime.now(UTC)

        return True

    async def complete_profile(
        self,
        user: User,
        first_name: str,
        last_name: str,
        birth_date,
        hashed_password: str,
    ) -> User:
        user.first_name = first_name
        user.last_name = last_name
        user.birth_date = birth_date
        user.hashed_password = hashed_password
        await self.db.flush()
        return user

    # ---------------------------
    # Unit of Work helpers
    # ---------------------------
    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, user: User):
        await self.db.refresh(user)
