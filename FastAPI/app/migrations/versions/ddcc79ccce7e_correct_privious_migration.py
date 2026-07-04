"""correct privious migration

Revision ID: ddcc79ccce7e
Revises: 80a9a5fb429f
Create Date: 2026-07-05 00:23:39.852240

"""

from collections.abc import Sequence

from alembic import op

# --- ایمپورت کدهای SQL ویو ---
from app.modules.catalog.models.product_view import (
    CREATE_PRODUCT_ADMIN_VIEW_SQL,
    DROP_PRODUCT_ADMIN_VIEW_SQL,
)

# revision identifiers, used by Alembic.
revision: str = "ddcc79ccce7e"
down_revision: str | Sequence[str] | None = "80a9a5fb429f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # اجرای مستقیم دستور CREATE VIEW در دیتابیس
    op.execute(CREATE_PRODUCT_ADMIN_VIEW_SQL)


def downgrade() -> None:
    """Downgrade schema."""
    # حذف VIEW در صورت نیاز به دانگرید (Rollback)
    op.execute(DROP_PRODUCT_ADMIN_VIEW_SQL)
