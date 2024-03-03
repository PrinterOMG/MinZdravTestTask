from core.repositories.users import BaseUsersRepository
from api.schemas.users import UserCreate


class UserService:
    def __init__(self, users_repository: BaseUsersRepository):
        self.users_repository = users_repository

    async def add(self, new_user: UserCreate):
        return await self.users_repository.add(new_user)

    async def get_all(self, offset, limit):
        return await self.users_repository.list(offset=offset, limit=limit)

    async def get_by_id(self, user_id):
        return await self.users_repository.get_by_id(user_id)

    async def get_by_username(self, username):
        return await self.users_repository.get_by_username(username)

    async def is_user_exists(self, user_id):
        return await self.users_repository.is_user_exists(user_id)
