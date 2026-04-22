from app.api.v1.dependencies import get_current_user_id, get_db_session
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import LoginRequest, TokenPair, UserCreate, UserRead
from app.modules.users.service import UserService
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate, db: AsyncSession = Depends(get_db_session)
) -> UserRead:
    service = UserService(UserRepository(db))
    user = await service.register(payload)
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenPair)
async def login_user(
    payload: LoginRequest, db: AsyncSession = Depends(get_db_session)
) -> TokenPair:
    service = UserService(UserRepository(db))
    return await service.login(payload)


@router.get("/me")
async def read_current_user(user_id: int = Depends(get_current_user_id)) -> dict[str, int]:
    return {"user_id": user_id}
