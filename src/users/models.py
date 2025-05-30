from typing import List, Optional

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

    all_owned_folders: Mapped[List["Folder"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    shared_editable_folders: Mapped[List["Folder"]] = relationship(
        secondary="folder_editing_access", back_populates="users_with_editing_access"
    )

    shared_viewable_folders: Mapped[List["Folder"]] = relationship(
        secondary="folder_view_access", back_populates="users_with_view_access"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
