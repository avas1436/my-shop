import asyncio
from alembic.config import Config
from alembic import command
from pathlib import Path


async def run_migrations():
    config_path = Path(__file__).resolve().parents[2] / "alembic.ini"
    alembic_cfg = Config(str(config_path))
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, command.upgrade, alembic_cfg, "head")
