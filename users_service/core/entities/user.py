from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserEntity(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str
    birthday: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
