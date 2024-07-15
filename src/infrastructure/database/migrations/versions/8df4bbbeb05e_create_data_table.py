"""create data table

Revision ID: 8df4bbbeb05e
Revises: 
Create Date: 2024-07-15 20:05:13.631439

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8df4bbbeb05e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("wind_speed", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("power", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "ambient_temperature", sa.DECIMAL(precision=10, scale=2), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("data")
