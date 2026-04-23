from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class PurposeOTP(str, Enum):
    LOGIN = "login"
    REGISTER = "register"
    RESET = "reset"


class InventoryStatus(str, Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
