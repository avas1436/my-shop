from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import UserRole
from app.core.database import get_db
from app.core.jwt import get_current_user
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.schemas.product import DraftProductCreate, ProductAdminRead
from app.modules.catalog.services.product import AdminProductService
from app.modules.users.models import User

router = APIRouter()


# @router.get("/", response_model=list[ProductAdminRead])
# async def list_products(
#     db: AsyncSession = Depends(get_db_session),
# ) -> list[ProductAdminRead]:
#     service = AdminProductService(AdminProductRepository(db))
#     products = await service.list_all()
#     return [ProductAdminRead.model_validate(product) for product in products]


@router.post(
    "/admin/createdraft",
    response_model=ProductAdminRead,
    status_code=status.HTTP_201_CREATED,
)
async def admin_create_product(
    payload: DraftProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],  # JWT guard
) -> ProductAdminRead:

    current, _ = current_user

    if not current.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="only admin",
        )

    service = AdminProductService(AdminProductRepository(db))

    product = await service.create(payload)

    return ProductAdminRead.model_validate(product)
