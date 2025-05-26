from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import Folder
from users.models import User


class FolderService:
    @staticmethod
    async def create_root(session: AsyncSession, user: User):
        current_folder = await FolderService.get_root(session, user)
        if not current_folder:
            folder = Folder(name="", is_root=True, owner=user)
            session.add(folder)
            await session.commit()
            return folder

        return current_folder

    @staticmethod
    async def get_root(session: AsyncSession, user: User):
        stmt = select(Folder).where(Folder.owner_id == user.id).where(Folder.is_root == True)
        result = await session.scalars(stmt)
        return result.first()

