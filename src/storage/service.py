import logging

from sqlalchemy import select, func, update, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from storage.models import Folder
from storage.schemas import FolderCreate, FolderUpdate
from users.models import User


class FolderService:


    @staticmethod
    async def update_child_paths(session: AsyncSession, folder):
        query = """
        WITH RECURSIVE folder_tree AS (
            SELECT 
                id, 
                name, 
                path, 
                parent_id
            FROM 
                folder
            WHERE 
                id = :folder_id

            UNION ALL

            SELECT 
                f.id, 
                f.name, 
                (ft.path || f.name || '/') AS path, 
                f.parent_id
            FROM 
                folder f
            JOIN 
                folder_tree ft ON f.parent_id = ft.id
        )
        UPDATE folder
        SET path = ft.path
        FROM folder_tree ft
        WHERE folder.id = ft.id
          AND folder.id != :folder_id;
        """

        await session.execute(
            text(query),
            {"folder_id": folder.id}
        )
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, folder_update_in: FolderUpdate, folder: Folder):

        for key, value in folder_update_in.model_dump().items():
            setattr(folder, key, value)

        await session.commit()
        return folder

    @staticmethod
    async def get_for_user_owner(session: AsyncSession, user: User, folder_id: int):
        stmt = (
            select(Folder)
            .where(Folder.owner_id == user.id)
            .where(Folder.id == folder_id)
            .options(selectinload(Folder.folders), selectinload(Folder.files))
        )

        result = await session.scalars(stmt)
        return result.first()

    @staticmethod
    async def get_by_name_and_parent(session: AsyncSession, name, parent_id):
        stmt = (
            select(Folder)
            .where(Folder.parent_id == parent_id)
            .where(Folder.name == name)
        )
        result = await session.scalars(stmt)
        return result.first()

    @staticmethod
    async def create(session: AsyncSession, folder_in: FolderCreate, parent=None):
        if parent is None:
            parent = await FolderService.get(session, folder_in.parent_id)
        folder = Folder(parent=parent, **folder_in.model_dump(exclude={"parent_id"}))
        session.add(folder)
        await session.commit()
        await session.refresh(folder)
        return folder

    @staticmethod
    async def get(session: AsyncSession, folder_id):
        return await session.get(
            Folder,
            folder_id,
            options=(selectinload(Folder.folders), selectinload(Folder.files)),
        )

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
        stmt = (
            select(Folder)
            .where(Folder.owner_id == user.id)
            .where(Folder.is_root == True)
            .options(selectinload(Folder.folders), selectinload(Folder.files))
        )
        result = await session.scalars(stmt)
        return result.first()


    @staticmethod
    async def delete(session: AsyncSession, folder: Folder):
        await session.delete(folder)
        await session.commit()
