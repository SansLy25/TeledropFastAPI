from fastapi import APIRouter

from core.db import SessionDp
from storage.schemas import FolderSchema
from users.auth import UserDp
from storage.service import FolderService

storage_rt = APIRouter(prefix="/storage")


@storage_rt.get("/folders/root", tags=["Папки"])
async def get_root(session: SessionDp, user: UserDp) -> FolderSchema:
    return await FolderService.get_root(session=session, user=user)

