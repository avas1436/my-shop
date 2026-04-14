def validate_price(value: float) -> float:
    if value < 0:
        raise ValueError("Price cannot be negative")
    return value
