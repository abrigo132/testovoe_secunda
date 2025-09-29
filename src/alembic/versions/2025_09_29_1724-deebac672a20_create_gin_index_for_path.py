"""create gin index for path

Revision ID: deebac672a20
Revises: 4cd675e9a5ea
Create Date: 2025-09-29 17:24:37.392127

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "deebac672a20"
down_revision: Union[str, Sequence[str], None] = "4cd675e9a5ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint("max_nesting_level_3", "activitys", "nlevel(path) <= 3")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("max_nesting_level_3", "activitys", type_="check")
