from math import ceil


def paginate(total: int, page: int, page_size: int) -> dict[str, int]:
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": ceil(total / page_size) if page_size else 0,
    }
