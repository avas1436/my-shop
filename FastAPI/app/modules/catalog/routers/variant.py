# app/modules/catalog/routers/variant.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.catalog.dependencies.variant import get_product_variant_service
from app.modules.catalog.schemas.variant import (
    ProductVariantCreate,
    ProductVariantRead,
    ProductVariantUpdate,
)
from app.modules.catalog.services.variant import ProductVariantService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


@router.post(
    "/",
    response_model=ProductVariantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_variant(
    request: Request,
    data: ProductVariantCreate,
    service: Annotated[ProductVariantService, Depends(get_product_variant_service)],
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
            )
        ),
    ],
):
    return await service.create_variant(data)


@router.get(
    "/list",
    response_model=PageResponse[dict],
    status_code=status.HTTP_200_OK,
)
async def list_variants(
    request: Request,
    service: Annotated[ProductVariantService, Depends(get_product_variant_service)],
    search: str | None = None,
    product_id: int | None = None,
    is_active: bool | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_variants(search, product_id, is_active, page, size)


@router.get(
    "/{variant_id}",
    response_model=ProductVariantRead,
    status_code=status.HTTP_200_OK,
)
async def get_variant(
    request: Request,
    variant_id: int,
    service: Annotated[ProductVariantService, Depends(get_product_variant_service)],
):
    return await service.get_variant(variant_id)


@router.put(
    "/{variant_id}",
    response_model=ProductVariantRead,
    status_code=status.HTTP_200_OK,
)
async def update_variant(
    request: Request,
    variant_id: int,
    data: ProductVariantUpdate,
    service: Annotated[ProductVariantService, Depends(get_product_variant_service)],
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
            )
        ),
    ],
):
    return await service.update_variant(variant_id, data)


@router.delete(
    "/{variant_id}",
    response_model=SuccessMessage,
    status_code=status.HTTP_200_OK,
)
async def delete_variant(
    request: Request,
    variant_id: int,
    service: Annotated[ProductVariantService, Depends(get_product_variant_service)],
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
            )
        ),
    ],
):
    await service.delete_variant(variant_id)
    return SuccessMessage(message="Product variant deleted successfully.")
