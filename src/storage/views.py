from fastapi import APIRouter, HTTPException

from core.db import SessionDp
from storage.schemas import RootFolderReadSchema, \
    FolderCreate, FolderReadSchema
from users.auth import UserDp
from storage.service import FolderService

storage_rt = APIRouter(prefix="/storage")


@storage_rt.get("/folders/root", tags=["Папки"])
async def get_root(session: SessionDp, user: UserDp) -> RootFolderReadSchema:
    return await FolderService.get_root(session=session, user=user)


@storage_rt.post("/folders", tags=["Папки"])
async def create_root(session: SessionDp, user: UserDp,
                      folder_in: FolderCreate) -> FolderReadSchema:
    parent = await FolderService.get(session, folder_in.parent_id)
    if parent is None:
        raise HTTPException(
            404, "Parent not found"
        )

    if parent.owner_id != user.id:
        raise HTTPException(
            403, "Parent folder doesn't belong to you"
        )

    if await FolderService.get_by_name_and_parent(session, folder_in.name,
                                                  folder_in.parent_id):
        raise HTTPException(
            409, "Folder with this name already exists in parent folder"
        )
    result = await FolderService.create(session, folder_in, parent)

    return result
