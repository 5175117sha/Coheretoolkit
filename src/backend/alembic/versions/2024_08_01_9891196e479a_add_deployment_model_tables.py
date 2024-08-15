"""Add agent deployment models
Revision ID: 9891196e479a
Revises: 7d85cfb9ec27
Create Date: 2024-08-01 15:03:43.575736

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9891196e479a"
down_revision: Union[str, None] = "7d85cfb9ec27"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "deployments",
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("deployment_class_name", sa.Text(), nullable=True),
        sa.Column("is_community", sa.Boolean(), nullable=False),
        sa.Column("default_deployment_config", sa.JSON(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="deployment_name_uc"),
    )
    op.create_table(
        "models",
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("cohere_name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("deployment_id", sa.String(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["deployment_id"], ["deployments.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "agent_deployment_model",
        sa.Column("agent_id", sa.String(), nullable=False),
        sa.Column("deployment_id", sa.String(), nullable=False),
        sa.Column("model_id", sa.String(), nullable=False),
        sa.Column("deployment_config", sa.JSON(), nullable=True),
        sa.Column("is_default_deployment", sa.Boolean(), nullable=False),
        sa.Column("is_default_model", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["deployment_id"], ["deployments.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "deployment_id", "agent_id", "model_id", name="deployment_agent_model_uc"
        ),
    )
    op.drop_column("agents", "deployment")
    op.drop_column("agents", "model")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "agents", sa.Column("model", sa.TEXT(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "agents",
        sa.Column("deployment", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.drop_table("agent_deployment_model")
    op.drop_table("models")
    op.drop_table("deployments")
    # ### end Alembic commands ###
