"""add product admin view

Revision ID: cb416294388e
Revises: 1df695b050c8
Create Date: 2026-07-04 02:41:43.772912

"""

from collections.abc import Sequence

from alembic import op

# --- ایمپورت کدهای SQL ویو ---
from app.modules.catalog.models.product_view import (
    CREATE_PRODUCT_ADMIN_VIEW_SQL,
    DROP_PRODUCT_ADMIN_VIEW_SQL,
)

# revision identifiers, used by Alembic.
revision: str = "cb416294388e"
down_revision: str | Sequence[str] | None = "1df695b050c8"
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
