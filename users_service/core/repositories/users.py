from abc import abstractmethod, ABC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.entities.user import UserEntity
from core.repositories.base import GenericAsyncRepository, GenericAsyncSQLAlchemyRepository
from database.models.user import UserModel


class BaseUsersRepository(GenericAsyncRepository[UserEntity], ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        raise NotImplementedError()

    @abstractmethod
    async def is_user_exists(self, id: UUID) -> bool:
        raise NotImplementedError()


class SQLAlchemyUsersRepository(GenericAsyncSQLAlchemyRepository[UserModel], BaseUsersRepository):
    def __init__(self, session: AsyncSession, model_cls=UserModel, entity=UserEntity) -> None:
        super().__init__(session, model_cls=model_cls, entity=entity)

    async def get_by_username(self, username: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.username == username)
        record = await self._session.execute(stmt)
        return record.scalar_one_or_none()

    async def is_user_exists(self, id: UUID) -> bool:
        stmt = select(UserModel.id).where(UserModel.id == id).exists().select()

        return await self._session.scalar(stmt)
