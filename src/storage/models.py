from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Integer,
    BigInteger,
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

from users.models import User
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

    @hybrid_property
    def is_root(self) -> bool:
        return self.parent_id is None

    def set_parent_owner(self) -> None:
        if self.parent:
            self.owner_id = self.parent.owner_id

    def __repr__(self) -> str:
        return f"<Folder(id={self.id}, name='{self.name}', path='{self.path}')>"


class File(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    size: Mapped[int] = mapped_column(Integer)
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
            self._path_cache = f"{self.parent.path}/{self.name}"
        return self._path_cache

    @validates("name")
    def _update_file_type(self, key: str, name: str) -> str:
        if hasattr(self, "name") and self.name != name:
            self._detect_file_type(name)
        return name

    def _detect_file_type(self, filename: str) -> None:
        file_types = getattr(self, "_cached_file_types", None)
        if file_types is None:
            self._cached_file_types = [
                {"type": "image", "extensions": ["jpg", "png", "gif"]},
                {"type": "document", "extensions": ["pdf", "docx"]},
            ]
            file_types = self._cached_file_types

        ext = filename.split(".")[-1].lower() if "." in filename else ""
        for ft in file_types:
            if ext in ft["extensions"]:
                self.type = ft["type"]
                return
        self.type = "other"


class FileVersion(Base):
    __tablename__ = "file_version"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[int] = mapped_column(Integer)
    telegram_file_id: Mapped[int] = mapped_column(BigInteger)
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"))

    file: Mapped["File"] = relationship(back_populates="versions")


@event.listens_for(Folder, "before_insert")
@event.listens_for(Folder, "before_update")
def _auto_set_folder_owner(mapper, connection, target: Folder):
    if not target.owner_id and target.parent:
        target.owner_id = target.parent.owner_id


@event.listens_for(File, "before_insert")
@event.listens_for(File, "before_update")
def _auto_set_file_type(mapper, connection, target: File):
    if not target.type:
        target._detect_file_type(target.name)
