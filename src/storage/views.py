from functools import update_wrapper

from fastapi import APIRouter, HTTPException

from core.db import SessionDp
from storage.schemas import RootFolderReadSchema, FolderCreate, \
    FolderReadSchema, FolderUpdate
from users.auth import UserDp
from storage.service import FolderService
from storage.dependencies import FolderReadPermission, FolderChangePermission, \
    change_folder_permission

storage_rt = APIRouter(prefix="/storage")


@storage_rt.get("/folders/root", tags=["Папки"])
async def get_root(session: SessionDp, user: UserDp) -> RootFolderReadSchema:
    return await FolderService.get_root(session=session, user=user)


@storage_rt.post("/folders", tags=["Папки"])
async def create_folder(
        session: SessionDp, user: UserDp, folder_in: FolderCreate,
) -> FolderReadSchema:
    parent = await change_folder_permission(folder_in.parent_id, user, session)

    if await FolderService.get_by_name_and_parent(
            session, folder_in.name, folder_in.parent_id
    ):
        raise HTTPException(
            409, "Folder with this name already exists in parent folder"
        )
    result = await FolderService.create(session, folder_in, parent)

    return result


@storage_rt.get("/folders/{folder_id}", tags=["Папки"])
async def get_folder(folder: FolderReadPermission) -> FolderReadSchema:
    return folder


@storage_rt.patch("/folders/{folder_id}", tags=["Папки"])
async def update_folder(
        session: SessionDp, folder: FolderChangePermission,
        folder_update: FolderUpdate
) -> FolderReadSchema:
    updated_folder = await FolderService.update(session, folder_update, folder)
    await FolderService.update_child_paths(session, updated_folder)
    return updated_folder


@storage_rt.delete("/folders/{folder_id}", tags=["Папки"], status_code=204)
async def delete_folder(
        session: SessionDp, folder: FolderChangePermission
):
    await FolderService.delete(session, folder)