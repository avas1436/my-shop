from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InventoryBase(BaseModel):
    quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)
    low_stock_alert: int = Field(default=5, ge=0)
    allow_backorder: bool = False


class InventoryCreate(InventoryBase):
    product_id: int


class InventoryUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=0)
    reserved_quantity: int | None = Field(default=None, ge=0)
    low_stock_alert: int | None = Field(default=None, ge=0)
    allow_backorder: bool | None = None


class InventoryRead(InventoryBase):
    id: int
    product_id: int
    updated_at: datetime | None = None
    available_quantity: int
    is_in_stock: bool

    model_config = ConfigDict(from_attributes=True)
