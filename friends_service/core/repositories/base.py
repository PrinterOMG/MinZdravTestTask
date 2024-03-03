from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, and_, Select
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import Base

T = TypeVar('T', bound=BaseModel)


class GenericAsyncRepository(Generic[T], ABC):
    def __init__(self, entity: Type[T]):
        self.entity = entity

    @abstractmethod
    async def get_by_id(self, id: UUID) -> T | None:
        """
        Get a single record by id

        :param id: Record id
        :return: Record or None
        """
        raise NotImplementedError()

    @abstractmethod
    async def list(self, offset: int = 0, limit: int = 100, **filters) -> list[T]:
        """
        Get a list of records

        :param limit:
        :param offset:
        :param filters: Filter conditions, several criteria are linked with a logical 'and'
        :raise ValueError: Invalid filter condition
        :return: List of records
        """
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        """
        Creates a new record

        :param record: The record to be created
        :return: The created record
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        """
        Updates an existing record.
        Searches for the record needed to update by the id attribute in the transferred record

        :param record: The record to be updated including record id
        :return: The updated record
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """
        Deletes a record by id

        :param id: Record id
        :return: None
        """
        raise NotImplementedError()


class GenericAsyncSQLAlchemyRepository(GenericAsyncRepository[T], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[Base], entity: Type[T]) -> None:
        """
        Creates a new repository instance

        :param session: SQLAlchemy async session
        :param model_cls: SQLAlchemy model class type
        """
        self._session = session
        self._model_cls = model_cls
        super().__init__(entity)

    def _construct_get_stmt(self, id: UUID) -> Select:
        """
        Creates a SELECT query for retrieving a single record

        :param id: Record id
        :return: SELECT statement
        """
        stmt = select(self._model_cls).where(self._model_cls.id == id)

        return stmt

    async def get_by_id(self, id: UUID) -> T | None:
        stmt = self._construct_get_stmt(id)
        result = await self._session.scalar(stmt)

        if result is None:
            return None

        return self.entity.model_validate(result)

    def _construct_list_stmt(self, offset, limit, **filters) -> Select:
        """
        Creates a SELECT query for retrieving a multiple records

        :param offset:
        :param limit:
        :param filters: Filter conditions, several criteria are linked with a logical 'and'
        :return: SELECT statement
        """
        stmt = select(self._model_cls)
        where_clauses = []
        for column, value in filters.items():
            if not hasattr(self._model_cls, column):
                raise ValueError(f'Invalid column name {column}')
            where_clauses.append(getattr(self._model_cls, column) == value)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))

        stmt = stmt.offset(offset).limit(limit)

        return stmt

    async def list(self, offset=0, limit=100, **filters) -> list[T]:
        stmt = self._construct_list_stmt(offset=offset, limit=limit, **filters)
        records = await self._session.scalars(stmt)

        return [self.entity.model_validate(record) for record in records.all()]

    async def add(self, record: T) -> T:
        record = self._model_cls(**record.model_dump())

        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        await self._session.commit()

        return self.entity.model_validate(record)

    async def update(self, record: T) -> T:
        record = self._model_cls(**record.model_dump())

        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        await self._session.commit()

        return self.entity.model_validate(record)

    async def delete(self, id: UUID) -> None:
        record = await self.get_by_id(id)

        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
            await self._session.commit()
