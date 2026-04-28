from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.core.database import get_db
from app.modules.catalog.repository.product import AdminProductRepository
from app.modules.catalog.schemas.product import DraftProductCreate, ProductAdminRead
from app.modules.catalog.services.product import AdminProductService
from app.modules.users.models import User

router = APIRouter()


# =========================================================
# Create a Draft Product
# =========================================================
@router.post(
    "/admin/createdraft",
    response_model=ProductAdminRead,
    status_code=status.HTTP_201_CREATED,
)
async def admin_create_draft_product(
    payload: DraftProductCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
) -> ProductAdminRead:

    service = AdminProductService(AdminProductRepository(db))

    product = await service.draft_create(payload)

    return ProductAdminRead.model_validate(product)


# =========================================================
# Soft Delete a Product
# =========================================================
@router.delete("/admin/products/{product_id}", status_code=204)
async def admin_soft_delete_product(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    service = AdminProductService(AdminProductRepository(db))
    deleted = await service.soft_delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="product not found")
    return None


# =========================================================
# Get List of Products
# =========================================================
# @router.get(
#     "/admin/products/{product_id}",
#     response_model=list[ProductAdminRead],
#     status_code=status.HTTP_200_OK,
# )
# async def list_products(
#     db: Annotated[AsyncSession, Depends(get_db)],
#     _: Annotated[User, Depends(require_admin)],
# ) -> list[ProductAdminRead]:
#     service = AdminProductService(AdminProductRepository(db))
#     products = await service.list_all()
#     return [ProductAdminRead.model_validate(product) for product in products]


# =========================================================
# Get a Product
# =========================================================
@router.get(
    "/admin/products/{product_id}",
    response_model=ProductAdminRead,
    status_code=status.HTTP_200_OK,
)
async def show_product(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
) -> ProductAdminRead:

    service = AdminProductService(AdminProductRepository(db))

    product = await service.get_product_admin(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return ProductAdminRead.model_validate(product)
