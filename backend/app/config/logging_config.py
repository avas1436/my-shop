from functools import lru_cache
import logging


@lru_cache
def setup_logger(level: str):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    return logging.getLogger("uvicorn.error")
