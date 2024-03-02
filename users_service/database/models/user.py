from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class UserModel(Base):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[date] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

