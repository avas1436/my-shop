import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import RedisCache
from app.common.pagination import PageMeta, PageResponse
from app.errors.errors import BadRequest, Conflict, NotFound
from app.modules.catalog.models.inventory import Inventory
from app.modules.catalog.repository.inventory import InventoryRepository
from app.modules.catalog.schemas.inventory import (
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
)


# --------------------------------------------------
# Inventory Service
# --------------------------------------------------
class InventoryService:
    def __init__(self, db: AsyncSession, cache: RedisCache):
        self.db = db
        self.cache = cache
        self.repo = InventoryRepository(db=db)

    async def create_inventory(self, data: InventoryCreate) -> Inventory:
        if not await self.repo.variant_exists(data.variant_id):
            raise NotFound(
                message="Variant not found.",
                code="VARIANT_NOT_FOUND",
            )

        exists = await self.repo.get_by_variant_id(data.variant_id)
        if exists:
            raise Conflict(
                message="Inventory for this variant already exists.",
                code="INVENTORY_ALREADY_EXISTS",
            )

        inventory = Inventory(**data.model_dump())
        return await self.repo.create(inventory)

    async def get_inventory(self, inventory_id: int) -> Inventory:
        inventory = await self.repo.get_by_id(inventory_id)
        if not inventory:
            raise NotFound(
                message="Inventory not found.",
                code="INVENTORY_NOT_FOUND",
            )
        return inventory

    async def list_inventories(
        self,
        variant_id: int | None,
        in_stock: bool | None,
        page: int,
        size: int,
    ) -> PageResponse[dict]:
        if page < 1 or size < 1 or size > 100:
            raise BadRequest(
                message="Invalid pagination values.",
                code="PAGINATION_INVALID_VALUES",
            )

        items, total = await self.repo.list_filtered(
            variant_id=variant_id,
            in_stock=in_stock,
            page=page,
            size=size,
        )

        pages = math.ceil(total / size) if total else 1

        return PageResponse(
            items=[InventoryRead.model_validate(x).model_dump() for x in items],
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

    async def update_inventory(
        self, inventory_id: int, data: InventoryUpdate
    ) -> Inventory:
        inventory = await self.repo.get_by_id(inventory_id)
        if not inventory:
            raise NotFound(
                message="Inventory not found.",
                code="INVENTORY_NOT_FOUND",
            )

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(inventory, field, value)

        return await self.repo.update(inventory)

    async def delete_inventory(self, inventory_id: int) -> None:
        inventory = await self.repo.get_by_id(inventory_id)
        if not inventory:
            raise NotFound(
                message="Inventory not found.",
                code="INVENTORY_NOT_FOUND",
            )

        await self.repo.delete(inventory)
