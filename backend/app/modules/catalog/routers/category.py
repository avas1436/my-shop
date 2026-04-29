from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.core.database import get_db
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

router = APIRouter()


# --------------------------------------------------
# Category Routes
# --------------------------------------------------
@router.post("/", response_model=CategoryRead)
async def create_category(
    data: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
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
    return await CategoryService(db=db, request=request).create_category(data)


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await CategoryService(db=db, request=request).get_category(category_id)


@router.get("/", response_model=PageResponse[dict])
async def list_categories(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    search: str | None = None,
    parent_id: int | None = None,
    is_active: bool | None = None,
    page: int = 1,
    size: int = 10,
):
    return await CategoryService(db=db, request=request).list_categories(
        search, parent_id, is_active, page, size
    )


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
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
    return await CategoryService(db=db, request=request).update_category(
        category_id, data
    )


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
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
    await CategoryService(db=db, request=request).delete_category(category_id)
    return {"detail": "Category deleted successfully."}


# --------------------------------------------------
# Product Category Routes
# --------------------------------------------------
@router.post("/{product_id}/categories/attach", response_model=ProductCategoryResult)
async def attach_categories(
    product_id: int,
    data: ProductCategoryAttach,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
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
            )
        ),
    ],
):
    return await ProductCategoryService(db, request).attach(
        product_id, data.category_ids
    )


@router.post("/{product_id}/categories/detach", response_model=ProductCategoryResult)
async def detach_categories(
    product_id: int,
    data: ProductCategoryDetach,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
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
            )
        ),
    ],
):
    return await ProductCategoryService(db, request).detach(
        product_id, data.category_ids
    )


@router.put("/{product_id}/categories/sync", response_model=ProductCategoryResult)
async def sync_categories(
    product_id: int,
    data: ProductCategorySync,
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
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
            )
        ),
    ],
):
    return await ProductCategoryService(db, request).sync(product_id, data.category_ids)
