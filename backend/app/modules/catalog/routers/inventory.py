from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.common.access_control import require_access
from app.common.enums import UserRole
from app.common.pagination import PageResponse
from app.common.responses import SuccessAPIRoute, SuccessMessage
from app.modules.catalog.dependencies.inventory import get_inventory_service
from app.modules.catalog.schemas.inventory import (
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
)
from app.modules.catalog.services.inventory import InventoryService
from app.modules.users.models import User

router = APIRouter(route_class=SuccessAPIRoute)


# --------------------------------------------------
# Inventory Model
# --------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=InventoryRead,
)
async def create_inventory(
    data: InventoryCreate,
    service: Annotated[InventoryService, Depends(get_inventory_service)],
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
    return await service.create_inventory(data)


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
    response_model=PageResponse[dict],
)
async def list_inventories(
    service: Annotated[InventoryService, Depends(get_inventory_service)],
    variant_id: int | None = None,
    in_stock: bool | None = None,
    page: int = 1,
    size: int = 10,
):
    return await service.list_inventories(variant_id, in_stock, page, size)


@router.get(
    "/{inventory_id}",
    status_code=status.HTTP_200_OK,
    response_model=InventoryRead,
)
async def get_inventory(
    inventory_id: int,
    service: Annotated[InventoryService, Depends(get_inventory_service)],
):
    return await service.get_inventory(inventory_id)


@router.put(
    "/{inventory_id}",
    status_code=status.HTTP_200_OK,
    response_model=InventoryRead,
)
async def update_inventory(
    inventory_id: int,
    data: InventoryUpdate,
    service: Annotated[InventoryService, Depends(get_inventory_service)],
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
    return await service.update_inventory(inventory_id, data)


@router.delete(
    "/{inventory_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessMessage,
)
async def delete_inventory(
    inventory_id: int,
    service: Annotated[InventoryService, Depends(get_inventory_service)],
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

    await service.delete_inventory(inventory_id)

    return SuccessMessage(message="Inventory deleted successfully.")
