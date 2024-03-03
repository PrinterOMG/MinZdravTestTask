import uuid
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import settings

engine = create_async_engine(settings.database_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


async def get_async_session_factory() -> async_sessionmaker:
    return async_session_maker


async def get_async_session(session_factory: Annotated[async_sessionmaker, Depends(get_async_session_factory)]):
    async with session_factory() as session:
        yield session
