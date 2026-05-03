# app/modules/catalog/routers/images.py
from datetime import timedelta
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.catalog.dependencies.image import get_image_service
from app.modules.catalog.schemas.image import (
    GetImage,
    ImageUpdate,
)
from app.modules.catalog.services.image import ImageService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


# =========================================================
# Add Image
# =========================================================
@router.post(
    "/admin/products/{product_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=GetImage,
)
async def upload_image(
    service: Annotated[ImageService, Depends(get_image_service)],
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
    "/admin/product/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[GetImage],
)
async def list_images(
    product_id: int,
    service: Annotated[ImageService, Depends(get_image_service)],
):
    return await service.get_product_images(product_id=product_id)


# =========================================================
# Get a Image
# =========================================================
@router.get(
    "/admin/image/{image_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetImage,
)
async def get_image(
    image_id: int,
    service: Annotated[ImageService, Depends(get_image_service)],
):
    return await service.get_image(image_id=image_id)


# =========================================================
# Update a Product Image
# =========================================================
@router.patch(
    "/admin/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetImage,
)
async def update_image(
    image_id: int,
    payload: ImageUpdate,
    service: Annotated[ImageService, Depends(get_image_service)],
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
    return await service.update_image(image_id=image_id, data=payload)


# =========================================================
# Delete a Image
# =========================================================
@router.delete(
    "/admin/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_image(
    image_id: int,
    service: Annotated[ImageService, Depends(get_image_service)],
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
    await service.delete_image(image_id=image_id)
    return SuccessMessage(message="Image deleted successfully.")
