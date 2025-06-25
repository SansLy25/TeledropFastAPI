from typing import Annotated, TypeVar

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionDp, get_session, Base
from storage.enums import Permission
from storage.models import File, Folder
from storage.service import FileService, FolderService
from users.auth import UserDp, get_or_create_user
from users.models import User

T = TypeVar("T", Folder, File)


async def get_folder_or_404(session: SessionDp, user: UserDp, folder_id: int) -> Folder:
    folder = await FolderService.get_for_user_owner(session, user, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found or access denied")
    return folder


async def get_file_or_404(session: SessionDp, file_id: int) -> File:
    file = await FileService.get(session, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found or access denied")
    return file


async def check_permission(
    obj: T, user: UserDp, permission: Permission, session: SessionDp
) -> T:
    if isinstance(obj, Folder):
        if permission == Permission.CHANGE and obj.is_root:
            raise HTTPException(status_code=403, detail="Cannot modify root folder")

    elif isinstance(obj, File):
        if obj.parent.owner_id != user.id:
            raise HTTPException(status_code=403, detail="File access denied")

    return obj


def get_object_by_permission(permission: Permission = Permission.READ, model: Folder | File = Folder):
    async def wrapper(
        object_id: int = Path(...),
        user: User = Depends(get_or_create_user),
        session: AsyncSession = Depends(get_session),
    ) -> Folder | File:
        if model == Folder:
            file_system_object = await get_folder_or_404(session, user,  object_id)
        else:
            file_system_object = await get_file_or_404(session, object_id)

        return await check_permission(file_system_object, user, permission, session)

    return wrapper


def get_folder_by_permission(permission: Permission = Permission.READ):
    """
    Шорткат для папок
    """
    return get_object_by_permission(permission, Folder)


def get_file_by_permission(permission: Permission = Permission.READ):
    """
    Шорткат для файлов, немножко дублирования)
    """
    return get_object_by_permission(permission, File)


FolderReadPermission = Annotated[Folder, Depends(get_folder_by_permission())]
FolderWritePermission = Annotated[
    Folder, Depends(get_folder_by_permission(permission=Permission.WRITE))
]
FolderChangePermission = Annotated[
    Folder, Depends(get_folder_by_permission(permission=Permission.CHANGE))
]

FileReadPermission = Annotated[
    File, Depends(get_file_by_permission(permission=Permission.READ))
]
FileChangePermission = Annotated[
    File, Depends(get_file_by_permission(permission=Permission.CHANGE))
]
