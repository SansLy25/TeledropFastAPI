from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    photo_url: Mapped[Optional[str]]


