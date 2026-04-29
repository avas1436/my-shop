from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.core.database import get_db
from app.modules.catalog.schemas.tag import TagCreate, TagRead, TagUpdate
from app.modules.catalog.services.tag import TagService
from app.modules.users.models import User

router = APIRouter()


@router.post("/admin", response_model=TagRead)
async def create_tag(
    data: TagCreate,
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
    return await TagService(db=db, request=request).create_tag(data)


@router.get("/admin/{tag_id}", response_model=TagRead)
async def get_tag(
    tag_id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await TagService(db=db, request=request).get_tag(tag_id)


@router.get("/admin", response_model=PageResponse[dict])
async def list_tags(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    search: str | None = None,
    tag_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    return await TagService(db=db, request=request).list_tags(
        search, tag_id, page, size
    )


@router.put("/admin/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: int,
    data: TagUpdate,
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
    return await TagService(db=db, request=request).update_tag(tag_id, data)


@router.delete("/admin/{tag_id}")
async def delete_tag(
    tag_id: int,
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
    await TagService(db=db, request=request).delete_tag(tag_id)
    return {"detail": "Tag deleted successfully."}
