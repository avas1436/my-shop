# app/core/storage/generate_url.py
from app.config.settings import get_settings

settings = get_settings()


def build_media_url(file_key: str) -> str:

    base = settings.media_base_url.rstrip("/")

    key = file_key.lstrip("/")

    return f"{base}/{key}"
