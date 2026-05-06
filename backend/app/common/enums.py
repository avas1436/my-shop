from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class PurposeOTP(StrEnum):
    LOGIN = "login"
    REGISTER = "register"
    RESET = "reset"


class InventoryStatus(StrEnum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"


class ProductStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"
    ARCHIVED = "archived"
