from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.admin_only import require_admin
from app.core.database import get_db
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
async def admin_create_draft_product(
    payload: DraftProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
) -> ProductAdminRead:

    service = AdminProductService(AdminProductRepository(db))

    product = await service.draft_create(payload)

    return ProductAdminRead.model_validate(product)
