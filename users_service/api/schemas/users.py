from datetime import datetime, date
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    birthday: date


class UserRead(UserBase):
    id: UUID
    created_at: datetime


class UserCreate(UserBase):
    username: Annotated[str, Field(min_length=4, max_length=20, description='Must be unique')]
    first_name: Annotated[str, Field(min_length=2, max_length=40)]
    last_name: Annotated[str, Field(min_length=2, max_length=40)]
