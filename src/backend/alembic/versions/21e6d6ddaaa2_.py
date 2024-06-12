"""empty message

Revision ID: 21e6d6ddaaa2
Revises: a9b07acef4e8
Create Date: 2024-06-12 17:45:27.296350

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "21e6d6ddaaa2"
down_revision: Union[str, None] = "a9b07acef4e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "agents", sa.Column("tool", postgresql.ARRAY(sa.Text()), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("agents", "tool")
    # ### end Alembic commands ###
