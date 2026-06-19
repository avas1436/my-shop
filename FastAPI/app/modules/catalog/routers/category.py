# app/modules/catalog/routers/category.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.catalog.dependencies.category import (
    get_category_service,
    get_product_category_service,
)
from app.modules.catalog.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    ProductCategoryAttach,
    ProductCategoryDetach,
    ProductCategoryResult,
    ProductCategorySync,
)
from app.modules.catalog.services.category import (
    CategoryService,
    ProductCategoryService,
)
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


# --------------------------------------------------
# Category Routes
# --------------------------------------------------
@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    request: Request,
    data: CategoryCreate,
    service: Annotated[CategoryService, Depends(get_category_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=5),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    return await service.create_category(data)


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    request: Request,
    category_id: int,
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await service.get_category(category_id)


@router.get(
    "/parents/{category_id}",
    response_model=list[CategoryRead],
    status_code=status.HTTP_200_OK,
)
async def get_category_parents(
    category_id: int,
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    return await service.get_category_parents(category_id)


@router.get("/", response_model=PageResponse[dict], status_code=status.HTTP_200_OK)
async def list_categories(
    request: Request,
    service: Annotated[CategoryService, Depends(get_category_service)],
    search: str | None = None,
    parent_id: int | None = None,
    is_active: bool | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_categories(search, parent_id, is_active, page, size)


@router.put(
    "/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK
)
async def update_category(
    request: Request,
    category_id: int,
    data: CategoryUpdate,
    service: Annotated[CategoryService, Depends(get_category_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=5),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    return await service.update_category(category_id, data)


@router.delete(
    "/{category_id}", response_model=SuccessMessage, status_code=status.HTTP_200_OK
)
async def delete_category(
    request: Request,
    category_id: int,
    service: Annotated[CategoryService, Depends(get_category_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=5),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            ),
        ),
    ],
):
    await service.delete_category(category_id)
    return SuccessMessage(message="Category deleted successfully.")


# --------------------------------------------------
# Product Category Routes
# --------------------------------------------------
@router.post(
    "/{product_id}/categories/attach",
    response_model=ProductCategoryResult,
    status_code=status.HTTP_200_OK,
)
async def attach_categories(
    request: Request,
    product_id: int,
    data: ProductCategoryAttach,
    service: Annotated[ProductCategoryService, Depends(get_product_category_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=5),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.attach(product_id, data.category_ids)


@router.post(
    "/{product_id}/categories/detach",
    response_model=ProductCategoryResult,
    status_code=status.HTTP_200_OK,
)
async def detach_categories(
    request: Request,
    product_id: int,
    data: ProductCategoryDetach,
    service: Annotated[ProductCategoryService, Depends(get_product_category_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=5),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.detach(product_id, data.category_ids)


@router.put(
    "/{product_id}/categories/sync",
    response_model=ProductCategoryResult,
    status_code=status.HTTP_200_OK,
)
async def sync_categories(
    request: Request,
    product_id: int,
    data: ProductCategorySync,
    service: Annotated[ProductCategoryService, Depends(get_product_category_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN],
                deny_roles=[UserRole.CUSTOMER],
                require_recent_login_within=timedelta(days=5),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name", "birth_date"),
            )
        ),
    ],
):
    return await service.sync(product_id, data.category_ids)
