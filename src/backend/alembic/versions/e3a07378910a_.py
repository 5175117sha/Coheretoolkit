"""empty message

Revision ID: e3a07378910a
Revises: ed17f144f4bf
Create Date: 2024-07-16 19:14:21.515376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3a07378910a'
down_revision: Union[str, None] = 'ed17f144f4bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('agent_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'files', 'agents', ['agent_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'files', type_='foreignkey')
    op.drop_column('files', 'agent_id')
    # ### end Alembic commands ###