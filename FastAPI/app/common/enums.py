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

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member
        return None


class ProductSortEnum(StrEnum):
    NEWEST = "newest"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    DISCOUNT_DESC = "discount_desc"


class CartStatus(StrEnum):
    ACTIVE = "active"  # فعال در حال تغییر
    ABANDONED = "abandoned"  # رها شده
    CONVERTED = "converted"  # تبدیل شده به سفارش
