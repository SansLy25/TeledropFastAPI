from fastapi import APIRouter, HTTPException

from core.db import SessionDp
from storage.dependencies import (
    FolderChangePermission,
    FolderReadPermission,
    FolderWritePermission,
    get_folder_permission,
)
from storage.enums import Permission
from storage.models import Folder
from storage.schemas import (
    FolderCreate,
    FolderMove,
    FolderReadSchema,
    FolderUpdate,
    RootFolderReadSchema,
)
from storage.service import FolderService
from users.auth import UserDp


storage_rt = APIRouter(prefix="/storage")


@storage_rt.get("/folders/root", tags=["Папки"])
async def get_root(session: SessionDp, user: UserDp) -> RootFolderReadSchema:
    return await FolderService.get_root(session=session, user=user)


@storage_rt.get("/folders/current", tags=["Папки"])
async def get_current_folder(user: UserDp, session: SessionDp) -> FolderReadSchema:
    return await FolderService.get_current_folder(user, session)


@storage_rt.post("/folders/{folder_id}/current", tags=["Папки"])
async def set_current_folder(
    folder: FolderReadPermission, user: UserDp, session: SessionDp
) -> FolderReadSchema:
    user.current_folder = folder
    session.add(user)
    await session.commit()
    return folder


@storage_rt.post("/folders", tags=["Папки"])
async def create_folder(
    session: SessionDp,
    user: UserDp,
    folder_in: FolderCreate,
) -> FolderReadSchema:
    parent = await get_folder_permission(Permission.WRITE)(
        folder_in.parent_id, user, session
    )

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
    session: SessionDp, folder: FolderChangePermission, folder_update: FolderUpdate
) -> FolderReadSchema:
    updated_folder = await FolderService.update(session, folder_update, folder)
    await FolderService.update_child_paths(session, updated_folder)
    return updated_folder


@storage_rt.post("/folders/{folder_id}/move", tags=["Папки"])
async def move_folder(
    session: SessionDp,
    moved_folder: FolderWritePermission,
    folder_move: FolderMove,
    user: UserDp,
) -> FolderReadSchema:
    new_parent = await get_folder_permission(Permission.WRITE)(
        folder_move.new_parent_id, user, session
    )

    if await FolderService.get_by_name_and_parent(
        session, moved_folder.name, folder_move.new_parent_id
    ):
        raise HTTPException(409, "Names conflict, rename folder")
    folder = await FolderService.move_folder(session, moved_folder, new_parent)
    await FolderService.update_child_paths(session, folder)
    return folder


@storage_rt.delete("/folders/{folder_id}", tags=["Папки"], status_code=204)
async def delete_folder(session: SessionDp, folder: FolderChangePermission):
    await FolderService.delete(session, folder)


# @storage_rt.get("/folders/{folder_id}", tags=["Файлы"])
# async def get_file(file: FileReadPermission):
#     return file


# @storage_rt.post("/folders/{folder_id}/copy", tags=["Папки"])
# async def move_folder(
#         session: SessionDp,
#         moved_folder: FolderWritePermission,
#         folder_copy: FolderMove,
#         user: UserDp,
# ):
#     new_parent = await write_folder_permission(folder_copy.new_parent_id, user, session)
#     folder = await FolderService.copy_folder(session, moved_folder, new_parent)
#     await FolderService.update_child_paths(session, folder.parent)
#     return folder

# --- Эндпоинты файлов ---
