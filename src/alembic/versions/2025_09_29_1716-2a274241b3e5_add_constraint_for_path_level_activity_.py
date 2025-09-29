"""add constraint for path level activity table

Revision ID: 2a274241b3e5
Revises: 4cd675e9a5ea
Create Date: 2025-09-29 17:16:12.784223

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2a274241b3e5"
down_revision: Union[str, Sequence[str], None] = "4cd675e9a5ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "idx_activities_path_gin",
        "activitys",
        ["path"],
        unique=False,
        postgresql_using="gin",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "idx_activities_path_gin", table_name="activitys", postgresql_using="gin"
    )
