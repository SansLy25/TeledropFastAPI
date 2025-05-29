from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionDp
from storage.models import Folder
from storage.service import FolderService
from users.auth import UserDp


async def read_folder_permission(folder_id: int, user: UserDp, session: SessionDp):
    # TODO: Добавить улучщенную логику прав
    folder = await FolderService.get_for_user_owner(session, user, folder_id)
    if not folder:
        raise HTTPException(404, "Folder not found or access denied")

    return folder


async def change_folder_permission(folder_id: int, user: UserDp, session: SessionDp):
    # TODO: Добавить улучщенную логику прав
    folder = await FolderService.get_for_user_owner(session, user, folder_id)
    if not folder:
        raise HTTPException(404, "Folder not found or access denied")

    if folder.is_root:
        raise HTTPException(403, "Access denied")

    return folder


FolderChangePermission = Annotated[Folder, Depends(change_folder_permission)]
FolderReadPermission = Annotated[Folder, Depends(read_folder_permission)]