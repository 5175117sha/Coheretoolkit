"""empty message

Revision ID: 32c5451e60e3
Revises: ec856fe2a19f
Create Date: 2024-07-24 20:35:49.950459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32c5451e60e3'
down_revision: Union[str, None] = 'ec856fe2a19f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'conversations', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'conversations', type_='unique')
    # ### end Alembic commands ###