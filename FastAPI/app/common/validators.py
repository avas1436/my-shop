def validate_price(value: int) -> int:
    if value < 0:
        raise ValueError("Price cannot be negative")
    return value
