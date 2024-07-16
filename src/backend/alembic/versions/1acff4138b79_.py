"""empty message

Revision ID: 1acff4138b79
Revises: a48691a80366
Create Date: 2024-07-09 15:27:44.022554

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1acff4138b79"
down_revision: Union[str, None] = "a48691a80366"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "agent_tool_metadata",
        "user_id",
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "agents",
        "user_id",
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "tool_auth",
        "user_id",
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=False,
    )

    op.drop_constraint(
        "documents_conversation_id_fkey", "documents", type_="foreignkey"
    )
    op.drop_constraint("files_conversation_id_fkey", "files", type_="foreignkey")
    op.drop_constraint("messages_conversation_id_fkey", "messages", type_="foreignkey")
    op.drop_constraint(
        "snapshots_conversation_id_fkey", "snapshots", type_="foreignkey"
    )
    op.drop_constraint("conversations_pkey", "conversations", type_="primary")

    op.create_unique_constraint(
        "conversation_id_user_id", "conversations", ["id", "user_id"]
    )
    op.create_primary_key("conversations_pkey", "conversations", ["id", "user_id"])
    op.create_index(
        "conversation_user_id_index", "conversations", ["id", "user_id"], unique=True
    )

    op.create_foreign_key(
        None, "agent_tool_metadata", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "agents", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "citations", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "conversations", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "document_conversation_id_user_id_fkey",
        "documents",
        "conversations",
        ["conversation_id", "user_id"],
        ["id", "user_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "file_conversation_id_user_id_fkey",
        "files",
        "conversations",
        ["conversation_id", "user_id"],
        ["id", "user_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "message_conversation_id_user_id_fkey",
        "messages",
        "conversations",
        ["conversation_id", "user_id"],
        ["id", "user_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None, "snapshot_access", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "snapshot_links", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "snapshot_conversation_id_user_id_fkey",
        "snapshots",
        "conversations",
        ["conversation_id", "user_id"],
        ["id", "user_id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None, "tool_auth", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_foreign_key(
        "snapshot_conversation_id_user_id_fkey", "snapshots", type_="foreignkey"
    )
    op.drop_foreign_key(None, "tool_auth", "users", type_="foreignkey")
    op.drop_foreign_key(None, "snapshot_links", "users", type_="foreignkey")
    op.drop_foreign_key(None, "snapshot_access", "users", type_="foreignkey")
    op.drop_foreign_key(
        "message_conversation_id_user_id_fkey", "messages", type_="foreignkey"
    )
    op.drop_foreign_key(
        "file_conversation_id_user_id_fkey", "files", type_="foreignkey"
    )
    op.drop_foreign_key(
        "document_conversation_id_user_id_fkey", "documents", type_="foreignkey"
    )
    op.drop_foreign_key(None, "conversations", "users", type_="foreignkey")
    op.drop_foreign_key(None, "citations", "users", type_="foreignkey")
    op.drop_foreign_key(None, "agents", "users", type_="foreignkey")
    op.drop_foreign_key(None, "agent_tool_metadata", "users", type_="foreignkey")

    op.drop_index("conversation_user_id_index", table_name="conversations")
    op.drop_constraint("conversations_pkey", "conversations", type_="primary")
    op.drop_constraint("conversation_id_user_id", "conversations", type_="unique")

    op.create_primary_key("conversations_pkey", "conversations", ["id"])
    op.create_foreign_key(
        "snapshots_conversation_id_fkey",
        "snapshots",
        "conversations",
        ["conversation_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "messages_conversation_id_fkey",
        "messages",
        "conversations",
        ["conversation_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "files_conversation_id_fkey",
        "files",
        "conversations",
        ["conversation_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "documents_conversation_id_fkey",
        "documents",
        "conversations",
        ["conversation_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.alter_column(
        "tool_auth",
        "user_id",
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=False,
    )
    op.alter_column(
        "agents",
        "user_id",
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=False,
    )
    op.alter_column(
        "agent_tool_metadata",
        "user_id",
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
