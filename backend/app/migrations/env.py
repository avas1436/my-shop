import sys
from pathlib import Path

# Dynamically add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from app.modules.categories.models import Category
from app.modules.comments.models import Comment
from app.modules.inventory.models import Inventory
from app.modules.products.models import Product
from app.modules.users.models import User

# import metadata from Base model
from app.core.database import Base, engine
from app.config.settings import get_settings

# Load Alembic configuration
config = context.config

# Load settings
settings = get_settings()

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:

    url = settings.database_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # detects column type changes
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable: AsyncEngine = engine

    async with connectable.connect() as connection:
        await connection.run_sync(_run_sync_migrations)

    await connectable.dispose()


def _run_sync_migrations(connection: Connection) -> None:
    """Helper function to run migrations in sync mode inside async engine."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------
# تابعی که خودت از main.py صدا میزنی
# -------------------------------
async def run_migrations():
    """
    Manually run Alembic migrations from inside the application (e.g., FastAPI lifespan).
    Uses the same logic Alembic CLI uses.
    """
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        await run_migrations_online()


# -------------------------------
# این قسمت برای Alembic CLI است
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
