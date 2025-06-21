from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    photo_url: Mapped[Optional[str]]
    current_folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder.id"))

    all_owned_folders: Mapped[List["Folder"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        foreign_keys="[Folder.owner_id]",
    )

    current_folder: Mapped["Folder"] = relationship(
        foreign_keys="[User.current_folder_id]",
        back_populates="current_users",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
