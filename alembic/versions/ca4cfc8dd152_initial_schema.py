"""initial schema

Revision ID: ca4cfc8dd152
Revises:
Create Date: 2026-09-13 10:58:14.567625

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ca4cfc8dd152"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

resource_status = sa.Enum("unread", "read", name="resourcestatus")


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_category_name"), "category", ["name"], unique=True)

    op.create_table(
        "source",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_source_name"), "source", ["name"], unique=True)

    op.create_table(
        "resource",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("status", resource_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["source.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_resource_status"), "resource", ["status"], unique=False)
    op.create_index(op.f("ix_resource_title"), "resource", ["title"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_resource_title"), table_name="resource")
    op.drop_index(op.f("ix_resource_status"), table_name="resource")
    op.drop_table("resource")
    op.drop_index(op.f("ix_source_name"), table_name="source")
    op.drop_table("source")
    op.drop_index(op.f("ix_category_name"), table_name="category")
    op.drop_table("category")
    resource_status.drop(op.get_bind(), checkfirst=True)
