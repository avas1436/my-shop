from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db_session
from app.modules.inventory.repository import InventoryRepository
from app.modules.inventory.schemas import InventoryCreate, InventoryRead
from app.modules.inventory.service import InventoryService


router = APIRouter()


@router.get("/", response_model=list[InventoryRead])
async def list_inventory(db: AsyncSession = Depends(get_db_session)) -> list[InventoryRead]:
    service = InventoryService(InventoryRepository(db))
    items = await service.list_all()
    return [InventoryRead.model_validate(item) for item in items]


@router.post("/", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
async def create_inventory(payload: InventoryCreate, db: AsyncSession = Depends(get_db_session)) -> InventoryRead:
    service = InventoryService(InventoryRepository(db))
    item = await service.create(payload)
    return InventoryRead.model_validate(item)
