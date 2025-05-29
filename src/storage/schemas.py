from typing import Optional

from pydantic import BaseModel, Field


class BaseFileFolderSchema(BaseModel):
    id: int
    name: str = Field(max_length=200)


class FileBaseSchema(BaseFileFolderSchema):
    path: str
    size: int


class FolderBaseSchema(BaseFileFolderSchema):
    pass


class FileNestedSchema(FileBaseSchema):
    pass


class FolderNestedSchema(FolderBaseSchema):
    pass


class FolderReadSchema(FolderBaseSchema):
    files: list[FileNestedSchema] = []
    folders: list[FolderNestedSchema] = []
    is_root: bool
    path: str
    parent_id: Optional[int] = None


class RootFolderReadSchema(BaseModel):
    id: int
    files: list[FileNestedSchema] = []
    folders: list[FolderNestedSchema] = []


class FolderCreate(BaseModel):
    name: str
    parent_id: int


class FolderUpdate(BaseModel):
    name: Optional[str] = None


class FolderMove(BaseModel):
    new_parent_id: int


class FileReadSchema(FileBaseSchema):
    parent_id: int
    type: str
