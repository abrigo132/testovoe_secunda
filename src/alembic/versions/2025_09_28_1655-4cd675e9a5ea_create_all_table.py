"""create all table

Revision ID: 4cd675e9a5ea
Revises:
Create Date: 2025-09-28 16:55:10.658902

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = "4cd675e9a5ea"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "activitys",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("path", sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_activitys_path"),
        "activitys",
        ["path"],
        unique=False,
        if_not_exists=True,
    )

    op.create_table(
        "buildings",
        sa.Column("address", sa.String(), nullable=False),
        sa.Column(
            "coords",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeogFromText",
                name="geography",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_buildings_coords",
        "buildings",
        ["coords"],
        unique=False,
        postgresql_using="gist",
        if_not_exists=True,
    )

    op.create_table(
        "organizations",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["buildings.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activitys.id"],
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )
    op.create_table(
        "phonenumbers",
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone_number"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("phonenumbers")
    op.drop_table("organization_activities")
    op.drop_table("organizations")
    op.drop_index(
        "idx_buildings_coords_gist", table_name="buildings", postgresql_using="gist"
    )
    op.drop_index(
        "idx_buildings_coords", table_name="buildings", postgresql_using="gist"
    )
    op.drop_table("buildings")
    op.drop_index(op.f("ix_activitys_path"), table_name="activitys")
    op.drop_table("activitys")
