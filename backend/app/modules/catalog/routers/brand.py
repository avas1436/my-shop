# app/modules/catalog/routers/brand.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.core.database import get_db
from app.modules.catalog.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.modules.catalog.services.brand import BrandService
from app.modules.users.models import User

router = APIRouter()


@router.post("/", response_model=BrandRead)
async def create_brand(
    data: BrandCreate,
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
    return await BrandService(db=db, request=request).create_brand(data)


@router.get("/{brand_id}", response_model=BrandRead)
async def get_brand(
    brand_id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    return await BrandService(db=db, request=request).get_brand(brand_id)


@router.get("/", response_model=PageResponse[dict])
async def list_brands(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    search: str | None = None,
    brand_id: int | None = None,
    page: int = 1,
    size: int = 10,
):

    return await BrandService(db=db, request=request).list_brands(
        search, brand_id, page, size
    )


@router.put("/{brand_id}", response_model=BrandRead)
async def update_brand(
    brand_id: int,
    data: BrandUpdate,
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
    return await BrandService(db=db, request=request).update_brand(brand_id, data)


@router.delete("/{brand_id}")
async def delete_brand(
    brand_id: int,
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
    await BrandService(db=db, request=request).delete_brand(brand_id)
    return {"detail": "Brand deleted successfully."}
