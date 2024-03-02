from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.users import SQLAlchemyUsersRepository
from core.services.users import UserService
from database.base import get_async_session


def get_users_service(async_session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserService:
    return UserService(SQLAlchemyUsersRepository(async_session))


users_service_dep = Annotated[UserService, Depends(get_users_service)]
