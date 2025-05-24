import mimetypes
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Integer,
    event, Table, Column
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates,
)
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional

from core.db import Base


folder_editing_access = Table(
    'folder_editing_access',
    Base.metadata,
    Column('folder_id', ForeignKey('folder.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)

folder_view_access = Table(
    'folder_view_access',
    Base.metadata,
    Column('folder_id', ForeignKey('folder.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)


class Folder(Base):
    __tablename__ = "folder"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder.id"),
                                                     nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_root: Mapped[bool] = mapped_column(default=False)
    _path_cache: Mapped[Optional[str]] = mapped_column("path", Text,
                                                       nullable=True)

    parent: Mapped[Optional["Folder"]] = relationship(
        remote_side=[id],
        back_populates="folders"
    )
    folders: Mapped[List["Folder"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    owner: Mapped["User"] = relationship(foreign_keys=[owner_id])
    users_with_editing_access: Mapped[List["User"]] = relationship(
        secondary=folder_editing_access,
        back_populates="shared_editable_folders"
    )
    users_with_view_access: Mapped[List["User"]] = relationship(
        secondary=folder_view_access,
        back_populates="shared_viewable_folders"
    )
    files: Mapped[List["File"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def path(self) -> str:
        if self._path_cache is None:
            self._compute_path()
        return self._path_cache

    def _compute_path(self) -> None:
        segments = []
        current = self
        while current.parent is not None:
            segments.append(current.name)
            current = current.parent
        self._path_cache = "/" + "/".join(reversed(segments))

    def set_parent_owner(self) -> None:
        if self.parent:
            self.owner_id = self.parent.owner_id

    def __repr__(self) -> str:
        return f"<Folder(id={self.id}, name='{self.name}', path='{self.path}')>"


class File(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    telegram_id: Mapped[int]
    type: Mapped[str] = mapped_column(String(50), default="other")
    parent_id: Mapped[int] = mapped_column(ForeignKey("folder.id"))
    _path_cache: Mapped[Optional[str]] = mapped_column("path", String(1000),
                                                       nullable=True)
    parent: Mapped["Folder"] = relationship(back_populates="files")
    versions: Mapped[List["FileVersion"]] = relationship(
        back_populates="file",
        cascade="all, delete-orphan",
        order_by="FileVersion.version"
    )

    @hybrid_property
    def path(self) -> str:
        if self._path_cache is None:
            self._path_cache = self.parent.path + self.name
        return self._path_cache

    @validates("name")
    def _update_file_type(self, key: str, name: str) -> str:
        if hasattr(self, "name") and self.name != name:
            self._detect_file_type(name)
        return name

    def _detect_file_type(self, filename: str) -> None:
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            self.type = "other/other"
        else:
            self.type = mime_type


class FileVersion(Base):
    __tablename__ = "file_version"

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[int]
    telegram_file_id: Mapped[int]
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"))
    size: Mapped[int]
    file: Mapped["File"] = relationship(back_populates="versions")


@event.listens_for(Folder, "before_insert")
def _auto_set_folder_owner(mapper, connection, target: Folder):
    if not target.owner_id and target.parent:
        target.owner_id = target.parent.owner_id


@event.listens_for(File, "before_insert")
@event.listens_for(File, "before_update")
def _auto_set_file_type(mapper, connection, target: File):
    if not target.type:
        target._detect_file_type(target.name)
