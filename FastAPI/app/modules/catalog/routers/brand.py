# app/modules/catalog/routers/brand.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.core.middlewares import limiter
from app.modules.catalog.dependencies.brand import get_brand_service
from app.modules.catalog.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.modules.catalog.services.brand import BrandService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


@router.post("/", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
async def create_brand(
    request: Request,
    data: BrandCreate,
    service: Annotated[BrandService, Depends(get_brand_service)],
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
    return await service.create_brand(data)


@router.get("/{brand_id}", response_model=BrandRead, status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def get_brand(
    request: Request,
    brand_id: int,
    service: Annotated[BrandService, Depends(get_brand_service)],
):
    return await service.get_brand(brand_id)


@router.get("/", response_model=PageResponse[dict], status_code=status.HTTP_200_OK)
async def list_brands(
    request: Request,
    service: Annotated[BrandService, Depends(get_brand_service)],
    search: str | None = None,
    brand_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_brands(search, brand_id, page, size)


@router.put("/{brand_id}", response_model=BrandRead, status_code=status.HTTP_200_OK)
async def update_brand(
    request: Request,
    brand_id: int,
    data: BrandUpdate,
    service: Annotated[BrandService, Depends(get_brand_service)],
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
    return await service.update_brand(brand_id, data)


@router.delete(
    "/{brand_id}", response_model=SuccessMessage, status_code=status.HTTP_200_OK
)
async def delete_brand(
    request: Request,
    brand_id: int,
    service: Annotated[BrandService, Depends(get_brand_service)],
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
    await service.delete_brand(brand_id)
    return SuccessMessage(message="Brand deleted successfully.")
