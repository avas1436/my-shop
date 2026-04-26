import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

# import metadata from Base model
from app.config.settings import get_settings  # noqa: E402
from app.core.database import Base, engine  # noqa: E402

# Load Alembic configuration
config = context.config

# Load settings
settings = get_settings()

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata

from app.modules.catalog.models.category import Category  # noqa: E402, F401, I001
from app.modules.catalog.models.category import ProductCategory  # noqa: E402, F401, I001
from app.modules.catalog.models.attribute import Attribute  # noqa: E402, F401, I001
from app.modules.catalog.models.attribute import ProductAttribute  # noqa: E402, F401, I001
from app.modules.catalog.models.attribute import ProductVariantAttribute  # noqa: E402, F401, I001
from app.modules.catalog.models.brand import Brand  # noqa: E402, F401, I001
from app.modules.catalog.models.image import ProductImage  # noqa: E402, F401, I001
from app.modules.catalog.models.product import Product  # noqa: E402, F401, I001
from app.modules.catalog.models.variant import ProductVariant  # noqa: E402, F401, I001
from app.modules.catalog.models.tag import ProductTag  # noqa: E402, F401, I001
from app.modules.catalog.models.tag import Tag  # noqa: E402, F401, I001
from app.modules.comments.models import Comment  # noqa: E402, F401, I001
from app.modules.inventory.models import Inventory  # noqa: E402, F401, I001
from app.modules.users.models import User  # noqa: E402, F401, I001


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
# async def run_migrations():
#     """
#     Manually run Alembic migrations from inside the application (e.g., FastAPI lifespan).
#     Uses the same logic Alembic CLI uses.
#     """
#     if context.is_offline_mode():
#         run_migrations_offline()
#     else:
#         await run_migrations_online()


# -------------------------------
# این قسمت برای Alembic CLI است
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
