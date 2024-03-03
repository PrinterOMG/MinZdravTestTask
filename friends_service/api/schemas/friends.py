from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class FriendRelationBase(BaseModel):
    initiator_id: UUID
    target_id: UUID
    tag: str


class FriendRelationRead(FriendRelationBase):
    id: UUID
    created_at: datetime


class FriendRelationCreate(FriendRelationBase):
    initiator_id: Annotated[UUID, Field(description='User who creates the friendship')]
    target_id: Annotated[UUID, Field(description='user with whom the friendship is created')]
    tag: Annotated[str, Field(description='Additional information about friendship')]
