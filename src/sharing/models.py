from datetime import datetime
from typing import Optional, Union

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from storage.enums import Permission
from storage.models import Folder, File


class Sharing(Base):
    __tablename__ = "sharing"
    author_id: Mapped[int] = mapped_column(ForeignKey("user"))
    folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder"))
    file_id: Mapped[Optional[int]] = mapped_column(ForeignKey("file"))
    access: Mapped[Permission]
    expired_date: Mapped[datetime]

    @hybrid_property
    def object_type(self) -> type[File | Folder]:
        return Folder if self.folder_id else File

    @hybrid_property
    def generate_link(self):
        pass
