from typing import Annotated

import aiohttp
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from core.repositories.friend_relations import SQLAlchemyFriendRelationRepository
from core.services.friends_relation import FriendRelationsService
from database.base import get_async_session
from utils.users_api import UsersAPI


def get_friend_relations_service(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> FriendRelationsService:
    return FriendRelationsService(SQLAlchemyFriendRelationRepository(async_session))


async def get_users_api() -> UsersAPI:
    async with aiohttp.ClientSession() as session:
        yield UsersAPI(settings.users_service_url, session)


friend_relations_service_dep = Annotated[FriendRelationsService, Depends(get_friend_relations_service)]
users_api_dep = Annotated[UsersAPI, Depends(get_users_api)]
