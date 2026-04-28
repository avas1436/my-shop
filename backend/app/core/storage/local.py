# app/core/storage/local.py
import os

# import aiofiles
from aiofiles import open

from app.config.settings import get_settings

settings = get_settings()


class LocalStorage:
    async def save(
        self, data: bytes, path: str, content_type: str | None = None
    ) -> str:

        full_path = os.path.join(settings.media_root, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        async with open(full_path, "wb") as f:
            await f.write(data)
        return path

    async def delete(self, path: str) -> None:
        full_path = os.path.join(settings.media_root, path)

        if os.path.exists(full_path):
            os.remove(full_path)
