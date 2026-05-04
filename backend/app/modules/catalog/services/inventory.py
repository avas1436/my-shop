from app.common.enums import InventoryStatus
from app.modules.inventory.models import Inventory
from app.modules.inventory.repository import InventoryRepository
from app.modules.inventory.schemas import InventoryCreate


class InventoryService:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    async def create(self, payload: InventoryCreate) -> Inventory:
        status = InventoryStatus.IN_STOCK if payload.quantity > 0 else InventoryStatus.OUT_OF_STOCK
        inventory = Inventory(
            product_id=payload.product_id,
            quantity=payload.quantity,
            status=status,
        )
        return await self.repository.create(inventory)

    async def list_all(self) -> list[Inventory]:
        return await self.repository.list_all()
