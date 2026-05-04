from datetime import datetime

from pydantic import BaseModel, Field


# --------------------------------------------------
# Inventory Schema
# --------------------------------------------------
class InventoryCreate(BaseModel):
    variant_id: int
    quantity: int = Field(0, ge=0)
    reserved_quantity: int = Field(0, ge=0)
    low_stock_alert: int = Field(5, ge=0)
    allow_backorder: bool = False


class InventoryUpdate(BaseModel):
    quantity: int | None = Field(None, ge=0)
    reserved_quantity: int | None = Field(None, ge=0)
    low_stock_alert: int | None = Field(None, ge=0)
    allow_backorder: bool | None = None


class InventoryRead(BaseModel):
    id: int
    variant_id: int
    quantity: int
    reserved_quantity: int
    low_stock_alert: int
    allow_backorder: bool
    updated_at: datetime | None
    available_quantity: int
    is_in_stock: bool

    class Config:
        from_attributes = True
