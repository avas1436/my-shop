# app/modules/catalog/routers/tag.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.catalog.dependencies.tag import (
    get_product_tag_service,
    get_tag_service,
)
from app.modules.catalog.schemas.tag import (
    ProductTagAttach,
    ProductTagDetach,
    ProductTagResult,
    ProductTagSync,
    TagCreate,
    TagRead,
    TagUpdate,
)
from app.modules.catalog.services.tag import ProductTagService, TagService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


# --------------------------------------------------
# Tag Routers
# --------------------------------------------------
@router.post("/admin", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    request: Request,
    data: TagCreate,
    service: Annotated[TagService, Depends(get_tag_service)],
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
    return await service.create_tag(data)


@router.get("/admin/{tag_id}", response_model=TagRead, status_code=status.HTTP_200_OK)
async def get_tag(
    request: Request,
    tag_id: int,
    service: Annotated[TagService, Depends(get_tag_service)],
):
    return await service.get_tag(tag_id)


@router.get("/admin", response_model=PageResponse[dict], status_code=status.HTTP_200_OK)
async def list_tags(
    request: Request,
    service: Annotated[TagService, Depends(get_tag_service)],
    search: str | None = None,
    tag_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_tags(search, tag_id, page, size)


@router.put("/admin/{tag_id}", response_model=TagRead, status_code=status.HTTP_200_OK)
async def update_tag(
    request: Request,
    tag_id: int,
    data: TagUpdate,
    service: Annotated[TagService, Depends(get_tag_service)],
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
    return await service.update_tag(tag_id, data)


@router.delete(
    "/admin/{tag_id}", response_model=SuccessMessage, status_code=status.HTTP_200_OK
)
async def delete_tag(
    request: Request,
    tag_id: int,
    service: Annotated[TagService, Depends(get_tag_service)],
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
    await service.delete_tag(tag_id)
    return SuccessMessage(message="Tag deleted successfully.")


# --------------------------------------------------
# Product Tag Routers
# --------------------------------------------------
@router.post(
    "/{product_id}/tags/attach",
    response_model=ProductTagResult,
    status_code=status.HTTP_200_OK,
)
async def attach_tags(
    request: Request,
    product_id: int,
    data: ProductTagAttach,
    service: Annotated[ProductTagService, Depends(get_product_tag_service)],
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
    return await service.attach(product_id, data.tag_ids)


@router.post(
    "/{product_id}/tags/detach",
    response_model=ProductTagResult,
    status_code=status.HTTP_200_OK,
)
async def detach_tags(
    request: Request,
    product_id: int,
    data: ProductTagDetach,
    service: Annotated[ProductTagService, Depends(get_product_tag_service)],
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
    return await service.detach(product_id, data.tag_ids)


@router.put(
    "/{product_id}/tags/sync",
    response_model=ProductTagResult,
    status_code=status.HTTP_200_OK,
)
async def sync_tags(
    request: Request,
    product_id: int,
    data: ProductTagSync,
    service: Annotated[ProductTagService, Depends(get_product_tag_service)],
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
    return await service.sync(product_id, data.tag_ids)
