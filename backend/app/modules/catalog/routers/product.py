# app/modules/catalog/routers/product.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.catalog.dependencies.product import get_admin_product_service
from app.modules.catalog.schemas.product import (
    DraftProductCreate,
    ProductAdminRead,
    ProductAdminUpdate,
    ProductSimpleRead,
)
from app.modules.catalog.services.product import AdminProductService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


# =========================================================
# Create a Draft Product
# =========================================================
@router.post(
    "/admin/createdraft",
    response_model=ProductSimpleRead,
    status_code=status.HTTP_201_CREATED,
)
async def admin_create_draft_product(
    payload: DraftProductCreate,
    service: Annotated[AdminProductService, Depends(get_admin_product_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=1),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
) -> ProductSimpleRead:
    product = await service.draft_create(payload)
    return ProductSimpleRead.model_validate(product)


# =========================================================
# Soft Delete a Product
# =========================================================
@router.delete(
    "/admin/products/soft/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductSimpleRead,
)
async def admin_soft_delete_product(
    product_id: int,
    service: Annotated[AdminProductService, Depends(get_admin_product_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=1),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    product = await service.soft_delete_product(product_id)

    return ProductSimpleRead.model_validate(product)


# =========================================================
# Hard Delete a Product
# =========================================================
@router.delete(
    "/admin/products/hard/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def admin_hard_delete_product(
    product_id: int,
    service: Annotated[AdminProductService, Depends(get_admin_product_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=1),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    await service.hard_delete_product(product_id)

    return SuccessMessage(message="Product deleted hardly.")


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
    service: Annotated[AdminProductService, Depends(get_admin_product_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=1),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    product = await service.get_product_admin(product_id)

    return product


# =========================================================
# Update Product
# =========================================================
@router.patch(
    "/admin/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductSimpleRead,
)
async def admin_patch_product(
    product_id: int,
    updates: ProductAdminUpdate,
    service: Annotated[AdminProductService, Depends(get_admin_product_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=1),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    product = await service.update_product(product_id=product_id, updates=updates)

    return ProductSimpleRead.model_validate(product)
