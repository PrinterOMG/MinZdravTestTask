from abc import abstractmethod, ABC
from uuid import UUID

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.entities.friend_relation import FriendRelationEntity
from core.repositories.base import GenericAsyncRepository, GenericAsyncSQLAlchemyRepository
from database.models import FriendRelationModel


class BaseFriendRelationRepository(GenericAsyncRepository[FriendRelationEntity], ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, offset, limit) -> list[FriendRelationEntity]:
        raise NotImplementedError()

    @abstractmethod
    async def get_friend_relation_by_users(
            self, first_user_id: UUID, second_user_id: UUID
    ) -> FriendRelationEntity | None:
        raise NotImplementedError()


class SQLAlchemyFriendRelationRepository(GenericAsyncSQLAlchemyRepository[FriendRelationModel],
                                         BaseFriendRelationRepository):
    def __init__(self, session: AsyncSession, model_cls=FriendRelationModel, entity=FriendRelationEntity) -> None:
        super().__init__(session, model_cls=model_cls, entity=entity)

    async def get_by_user_id(self, user_id: UUID, offset, limit) -> list[FriendRelationEntity]:
        stmt = (
            select(FriendRelationModel)
            .where(or_(FriendRelationModel.initiator_id == user_id, FriendRelationModel.target_id == user_id))
            .offset(offset)
            .limit(limit)
        )

        records = await self._session.scalars(stmt)
        return [self.entity.model_validate(record) for record in records.all()]

    async def get_friend_relation_by_users(
            self, first_user_id: UUID, second_user_id: UUID
    ) -> FriendRelationEntity | None:
        stmt = (
            select(FriendRelationModel)
            .where(
                or_(
                    and_(
                        FriendRelationModel.initiator_id == first_user_id,
                        FriendRelationModel.target_id == second_user_id
                    ),
                    and_(
                        FriendRelationModel.initiator_id == second_user_id,
                        FriendRelationModel.target_id == first_user_id
                    )
                )
            )
        )
        result = await self._session.scalar(stmt)
        if result is None:
            return None

        return self.entity.model_validate(result)
