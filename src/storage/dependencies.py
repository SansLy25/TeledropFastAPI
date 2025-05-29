from typing import Annotated, TypeVar
from enum import Enum, auto
from fastapi import HTTPException, Depends
from core.db import SessionDp
from storage.models import Folder, File
from storage.service import FolderService, FileService
from users.auth import UserDp

T = TypeVar('T', Folder, File)


class Permission(Enum):
    READ = auto()
    WRITE = auto()
    CHANGE = auto()


async def get_folder_or_404(session: SessionDp, user: UserDp,
                            folder_id: int) -> Folder:
    folder = await FolderService.get_for_user_owner(session, user, folder_id)
    if not folder:
        raise HTTPException(status_code=404,
                            detail="Folder not found or access denied")
    return folder


async def get_file_or_404(session: SessionDp, file_id: int) -> File:
    file = await FileService.get(session, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found or access denied")
    return file


async def check_permission(
        obj: T,
        user: UserDp,
        permission: Permission,
        session: SessionDp
) -> T:

    if isinstance(obj, Folder):
        if permission == Permission.CHANGE and obj.is_root:
            raise HTTPException(status_code=403,
                                detail="Cannot modify root folder")

    elif isinstance(obj, File):
        if obj.parent.owner_id != user.id:
            raise HTTPException(status_code=403, detail="File access denied")


    return obj


async def folder_permission(
        folder_id: int,
        user: UserDp,
        session: SessionDp,
        permission: Permission
) -> Folder:
    folder = await get_folder_or_404(session, user, folder_id)
    return await check_permission(folder, user, permission, session)


async def file_permission(
        file_id: int,
        user: UserDp,
        session: SessionDp,
        permission: Permission
) -> File:
    file = await get_file_or_404(session, file_id)
    return await check_permission(file, user, permission, session)



FolderReadPermission = Annotated[
    Folder, Depends(lambda: folder_permission(permission=Permission.READ))]
FolderWritePermission = Annotated[
    Folder, Depends(lambda: folder_permission(permission=Permission.WRITE))]
FolderChangePermission = Annotated[
    Folder, Depends(lambda: folder_permission(permission=Permission.CHANGE))]

FileReadPermission = Annotated[
    File, Depends(lambda: file_permission(permission=Permission.READ))]
FileWritePermission = Annotated[
    File, Depends(lambda: file_permission(permission=Permission.WRITE))]