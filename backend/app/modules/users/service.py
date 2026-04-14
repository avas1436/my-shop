from app.common.enums import UserRole
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import LoginRequest, TokenPair, UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, payload: UserCreate) -> User:
        existing_user = await self.repository.get_by_email(payload.email)
        if existing_user:
            raise AppException("User already exists", 409)

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            role=UserRole.CUSTOMER,
        )
        return await self.repository.create(user)

    async def login(self, payload: LoginRequest) -> TokenPair:
        user = await self.repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise AppException("Invalid credentials", 401)

        subject = str(user.id)
        return TokenPair(
            access_token=create_access_token(subject),
            refresh_token=create_refresh_token(subject),
        )
