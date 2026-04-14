from pydantic import BaseModel

from app.common.enums import InventoryStatus


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int


class InventoryRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: InventoryStatus

    class Config:
        from_attributes = True
