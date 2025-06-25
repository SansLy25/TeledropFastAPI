from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import Folder, File
from storage.service import FolderService, FileService

async def check_conflicts(
        parent: int | Folder,
        name: str,
        session: AsyncSession
):
    if isinstance(parent, int):
        parent = await FolderService.get(session, parent)

    if (await FileService.get_by_parent_and_name(session, parent, name) or
        await FolderService.get_by_name_and_parent(session, name, parent.id)):
        raise HTTPException(409, "Object in this folder with this name already exists")