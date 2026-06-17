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

    # دریافت آیدی محصول برای حذف کلید ها
    async def _get_product_id_from_variant(
        self,
        variant_id: int,
    ) -> int | None:

        product_id = await self.repo.get_product_id(variant_id)

        if not product_id:
            return None

        return product_id

    # -------------------------
    # create inventory
    # -------------------------
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
        created_inventory = await self.repo.create(inventory)

        if self.cache.is_available():
            await self.cache.invalidate_lists()

            product_id = await self._get_product_id_from_variant(data.variant_id)
            if product_id:
                await self.cache.invalidate_key("admin", "full", product_id)
                await self.cache.invalidate_key("user", "full", product_id)
                await self.cache.invalidate_key("homepage")

        return created_inventory

    # -------------------------
    # get inventory
    # -------------------------
    async def get_inventory(self, inventory_id: int) -> Inventory:
        if self.cache.is_available():
            cached = await self.cache.get("inventory", inventory_id)
            if cached is not None:
                return cached

        inventory = await self.repo.get_by_id(inventory_id)
        if not inventory:
            raise NotFound(
                message="Inventory not found.",
                code="INVENTORY_NOT_FOUND",
            )
        payload = InventoryRead.model_validate(inventory).model_dump(mode="json")

        if self.cache.is_available():
            await self.cache.set("inventory", inventory_id, payload=payload)

        return payload

    # -------------------------
    # list inventories
    # -------------------------
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

        if self.cache.is_available():
            cached = await self.cache.get_list(
                "list",
                "inventory",
                variant_id,
                in_stock,
                page,
                size,
            )
            if cached is not None:
                return PageResponse(**cached)

        items, total = await self.repo.list_filtered(
            variant_id=variant_id,
            in_stock=in_stock,
            page=page,
            size=size,
        )

        pages = math.ceil(total / size) if total else 1
        response_items = [
            InventoryRead.model_validate(x).model_dump(mode="json") for x in items
        ]

        resp = PageResponse(
            items=response_items,
            meta=PageMeta(page=page, size=size, total=total, pages=pages),
        )

        if self.cache.is_available():
            await self.cache.set_list(
                "list",
                "inventory",
                variant_id,
                in_stock,
                page,
                size,
                payload=resp.model_dump(mode="json"),
            )

        return resp

    # -------------------------
    # update inventory
    # -------------------------
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

        updated_inventory = await self.repo.update(inventory)

        # Cache Invalidation
        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("inventory", inventory_id)

            product_id = await self._get_product_id_from_variant(inventory.variant_id)
            print(product_id)
            if product_id:
                await self.cache.invalidate_key("admin", "full", product_id)
                await self.cache.invalidate_key("user", "full", product_id)
                await self.cache.invalidate_key("homepage")

        return updated_inventory

    # -------------------------
    # delete inventory
    # -------------------------
    async def delete_inventory(self, inventory_id: int) -> None:
        inventory = await self.repo.get_by_id(inventory_id)
        if not inventory:
            raise NotFound(
                message="Inventory not found.",
                code="INVENTORY_NOT_FOUND",
            )

        variant_id = inventory.variant_id
        await self.repo.delete(inventory)

        # Cache Invalidation
        if self.cache.is_available():
            await self.cache.invalidate_lists()
            await self.cache.invalidate_key("inventory", inventory_id)

            product_id = await self._get_product_id_from_variant(variant_id)
            if product_id:
                await self.cache.invalidate_key("admin", "full", product_id)
                await self.cache.invalidate_key("user", "full", product_id)
                await self.cache.invalidate_key("homepage")
