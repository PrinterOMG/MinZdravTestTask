from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FriendRelationEntity(BaseModel):
    id: UUID
    initiator_id: UUID
    target_id: UUID
    tag: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
