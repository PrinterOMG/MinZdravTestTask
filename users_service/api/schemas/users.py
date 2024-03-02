from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    birthday: date
    created_at: datetime


class UserRead(UserBase):
    id: UUID


class UserCreate(UserBase):
    pass
