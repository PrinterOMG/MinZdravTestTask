from abc import abstractmethod, ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.base import GenericAsyncRepository, GenericAsyncSQLAlchemyRepository
from database.models.user import UserModel


class BaseUsersRepository(GenericAsyncRepository[UserModel], ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> UserModel | None:
        raise NotImplementedError()


class SQLAlchemyUsersRepository(GenericAsyncSQLAlchemyRepository[UserModel], BaseUsersRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_username(self, phone: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.phone == phone)
        record = await self._session.execute(stmt)
        return record.scalar_one_or_none()
