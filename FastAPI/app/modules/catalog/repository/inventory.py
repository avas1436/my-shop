from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models.inventory import Inventory
from app.modules.catalog.models.variant import ProductVariant


# --------------------------------------------------
# Inventory Repository
# --------------------------------------------------
class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def variant_exists(self, variant_id: int) -> bool:
        q = select(ProductVariant.id).where(ProductVariant.id == variant_id)
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def get_by_id(self, inventory_id: int) -> Inventory | None:
        result = await self.db.execute(
            select(Inventory).where(Inventory.id == inventory_id)
        )
        return result.scalar_one_or_none()

    async def get_by_variant_id(self, variant_id: int) -> Inventory | None:
        result = await self.db.execute(
            select(Inventory).where(Inventory.variant_id == variant_id)
        )
        return result.scalar_one_or_none()

    async def get_product_id(self, inventory_id: int) -> int | None:
        result = await self.db.execute(
            select(ProductVariant.product_id)
            .join(
                Inventory,
                Inventory.variant_id == ProductVariant.id,
            )
            .where(Inventory.id == inventory_id)
        )

        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        variant_id: int | None,
        in_stock: bool | None,
        page: int,
        size: int,
    ) -> tuple[list[Inventory], int]:
        query = select(Inventory)
        count_query = select(func.count(Inventory.id))

        if variant_id:
            query = query.where(Inventory.variant_id == variant_id)
            count_query = count_query.where(Inventory.variant_id == variant_id)

        if in_stock is not None:
            available_expr = Inventory.quantity - Inventory.reserved_quantity
            in_stock_expr = (available_expr > 0) | (Inventory.allow_backorder.is_(True))
            if in_stock:
                query = query.where(in_stock_expr)
                count_query = count_query.where(in_stock_expr)
            else:
                query = query.where(~in_stock_expr)
                count_query = count_query.where(~in_stock_expr)

        query = query.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(query)).scalars().all()
        total = (await self.db.execute(count_query)).scalar_one()
        return list(items), total

    async def create(self, inventory: Inventory) -> Inventory:
        self.db.add(inventory)
        await self.db.commit()
        await self.db.refresh(inventory)
        return inventory

    async def update(self, inventory: Inventory) -> Inventory:
        self.db.add(inventory)
        await self.db.commit()
        await self.db.refresh(inventory)
        return inventory

    async def delete(self, inventory: Inventory) -> None:
        await self.db.delete(inventory)
        await self.db.commit()
