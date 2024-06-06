"""empty message

Revision ID: f5819b10ef2a
Revises: 3247f8fd3f71
Create Date: 2024-06-06 16:13:32.066454

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f5819b10ef2a"
down_revision: Union[str, None] = "3247f8fd3f71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("files", sa.Column("file_content", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("files", "file_content")
    # ### end Alembic commands ###
