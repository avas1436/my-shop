from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db_session
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schemas import CategoryCreate, CategoryRead
from app.modules.categories.service import CategoryService


router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db_session)) -> list[CategoryRead]:
    service = CategoryService(CategoryRepository(db))
    categories = await service.list_all()
    return [CategoryRead.model_validate(category) for category in categories]


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db_session)) -> CategoryRead:
    service = CategoryService(CategoryRepository(db))
    category = await service.create(payload)
    return CategoryRead.model_validate(category)
