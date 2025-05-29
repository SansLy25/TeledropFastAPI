from typing import Annotated, TypeVar
from fastapi import HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionDp, get_session
from storage.models import Folder, File
from storage.service import FolderService, FileService
from users.auth import UserDp, get_or_create_user
from storage.enums import Permission
from users.models import User

T = TypeVar('T', Folder, File)


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
        folder_id: int = Path(...),
        user: User = Depends(get_or_create_user),
        session: AsyncSession = Depends(get_session),
        permission: Permission = Permission.READ
) -> Folder:
    folder = await get_folder_or_404(session, user, folder_id)
    return await check_permission(folder, user, permission, session)


async def file_permission(
        file_id: int = Path(...),
        user: User = Depends(get_or_create_user),
        session: AsyncSession = Depends(get_session),
        permission: Permission = Permission.READ
) -> File:
    file = await get_file_or_404(session, file_id)
    return await check_permission(file, user, permission, session)


FolderReadPermission = Annotated[Folder, Depends(folder_permission)]
FolderWritePermission = Annotated[Folder, Depends(lambda: folder_permission(permission=Permission.WRITE))]
FolderChangePermission = Annotated[Folder, Depends(lambda: folder_permission(permission=Permission.CHANGE))]

FileReadPermission = Annotated[File, Depends(file_permission)]
FileWritePermission = Annotated[File, Depends(lambda: file_permission(permission=Permission.WRITE))]