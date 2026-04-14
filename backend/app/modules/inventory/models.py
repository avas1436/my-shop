from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import InventoryStatus
from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[InventoryStatus] = mapped_column(default=InventoryStatus.IN_STOCK)

    product = relationship("Product", back_populates="inventory")
