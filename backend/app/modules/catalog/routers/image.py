# app/modules/catalog/routers/images.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.core.database import get_db
from app.modules.catalog.repository.image import ImageRepository
from app.modules.catalog.schemas.image import (
    GetImage,
    ImageUpdate,
)
from app.modules.catalog.services.image import ImageService
from app.modules.users.models import User

router = APIRouter()


def get_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return ImageService(ImageRepository(db))


# =========================================================
# Add Image
# =========================================================
@router.post(
    "/admin/products/{product_id}/images",
    status_code=status.HTTP_201_CREATED,
    response_model=GetImage,
)
async def upload_image(
    service: Annotated[ImageService, Depends(get_service)],
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
    product_id: int,
    file: Annotated[UploadFile, File(...)],
    alt_text: str | None = Form(None),
    is_primary: bool = Form(False),
    sort_order: int = Form(0),
):

    return await service.add_image(
        product_id=product_id,
        file=file,
        alt_text=alt_text,
        is_primary=is_primary,
        sort_order=sort_order,
    )


# =========================================================
# Get Images of a Product
# =========================================================
@router.get(
    "/admin/products/{product_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=list[GetImage],
)
async def list_images(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    repo = ImageRepository(db)

    return await repo.list_by_product(product_id)


# =========================================================
# Update a Product Image
# =========================================================
@router.patch(
    "/admin/products/{product_id}/images/{image_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetImage,
)
async def update_image(
    product_id: int,
    image_id: int,
    payload: ImageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: Annotated[ImageService, Depends(get_service)],
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

    repo = ImageRepository(db)

    img = await repo.get(image_id)

    if not img or img.product_id != product_id:
        raise HTTPException(status_code=404, detail="Image not found")

    return await service.update_image(img, **payload.model_dump(exclude_unset=True))


# =========================================================
# Delete a Image
# =========================================================
@router.delete(
    "/admin/products/{product_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_image(
    product_id: int,
    image_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    service: Annotated[ImageService, Depends(get_service)],
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

    repo = ImageRepository(db)

    img = await repo.get(image_id)

    if not img or img.product_id != product_id:
        raise HTTPException(status_code=404, detail="Image not found")

    await service.delete_image(img)
