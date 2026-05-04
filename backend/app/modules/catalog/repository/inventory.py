from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Inventory


class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, inventory: Inventory) -> Inventory:
        self.db.add(inventory)
        await self.db.commit()
        await self.db.refresh(inventory)
        return inventory

    async def list_all(self) -> list[Inventory]:
        result = await self.db.execute(select(Inventory).order_by(Inventory.id.desc()))
        return list(result.scalars().all())
