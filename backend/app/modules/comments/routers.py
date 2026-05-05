# app/modules/comments/routerspy
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.comments.dependencies import get_comment_service
from app.modules.comments.schemas import CommentCreate, CommentRead, CommentUpdate
from app.modules.comments.service import CommentService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


# --------------------------------------------------
# Comment
# --------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentRead,
)
async def create_comment(
    data: CommentCreate,
    service: Annotated[CommentService, Depends(get_comment_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN, UserRole.CUSTOMER],
                deny_roles=[],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name"),
            )
        ),
    ],
):
    return await service.create_comment(data)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PageResponse[dict],
)
async def list_comments(
    service: Annotated[CommentService, Depends(get_comment_service)],
    user_id: int | None = None,
    product_id: int | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_comments(
        user_id=user_id,
        product_id=product_id,
        page=page,
        size=size,
    )


@router.get(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentRead,
)
async def get_comment(
    comment_id: int,
    service: Annotated[CommentService, Depends(get_comment_service)],
):
    return await service.get_comment(comment_id)


@router.put(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentRead,
)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    service: Annotated[CommentService, Depends(get_comment_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN, UserRole.CUSTOMER],
                deny_roles=[],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name"),
            )
        ),
    ],
):
    return await service.update_comment(comment_id, data)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_comment(
    comment_id: int,
    service: Annotated[CommentService, Depends(get_comment_service)],
    _: Annotated[
        User,
        Depends(
            require_access(
                allowed_roles=[UserRole.ADMIN, UserRole.CUSTOMER],
                deny_roles=[],
                require_recent_login_within=timedelta(minutes=30),
                require_password=True,
                require_profile_complete=True,
                profile_required_fields=("first_name", "last_name"),
            )
        ),
    ],
):
    await service.delete_comment(comment_id)
    return SuccessMessage(message="Comment deleted successfully.")
