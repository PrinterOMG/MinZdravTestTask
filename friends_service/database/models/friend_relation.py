from datetime import datetime
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class FriendRelationModel(Base):
    __tablename__ = 'friend_relation'

    initiator_id: Mapped[UUID] = mapped_column(nullable=False)
    target_id: Mapped[UUID] = mapped_column(nullable=False)
    tag: Mapped[str] = mapped_column(nullable=False, default='')

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(initiator_id, target_id, name='uniq_friend_relation'),
    )
