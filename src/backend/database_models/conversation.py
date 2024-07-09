from typing import List, Optional

from sqlalchemy import ForeignKey, Index, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base
from backend.database_models.file import File
from backend.database_models.message import Message
from uuid import uuid4


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String, default="New Conversation")
    description: Mapped[str] = mapped_column(String, nullable=True, default=None)

    text_messages: Mapped[List["Message"]] = relationship()
    files: Mapped[List["File"]] = relationship()
    agent_id: Mapped[str] = mapped_column(
        ForeignKey("agents.id", ondelete="CASCADE"), nullable=True
    )
    organization_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(
            "organizations.id",
            name="conversations_organization_id_fkey",
            ondelete="CASCADE",
        )
    )

    @property
    def messages(self):
        return sorted(self.text_messages, key=lambda x: x.created_at)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'user_id', name='conversation_pk'),
        Index("conversation_user_agent_index", "user_id", "agent_id"),
    )
