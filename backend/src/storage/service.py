from datetime import datetime
from typing import Tuple

from sqlalchemy import select, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from storage.models import File, Folder, FileVersion
from storage.schemas import FolderCreate, FolderUpdate, FileUpdate
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

        await session.execute(text(query), {"folder_id": folder.id})
        await session.commit()

    @staticmethod
    async def update(
        session: AsyncSession, folder_update_in: FolderUpdate, folder: Folder
    ):
        if await FolderService.get_by_name_and_parent(
            session, folder.name, folder.parent_id
        ):
            pass
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
    async def get_current_folder(user: User, session: AsyncSession):

        if user.current_folder is not None:
            folder = user.current_folder
            await session.refresh(folder)
            return folder
        # If current folder is None, return root folder
        return await FolderService.get_root(session, user)

    @staticmethod
    async def delete(session: AsyncSession, folder: Folder):
        await session.delete(folder)
        await session.commit()

    @staticmethod
    async def move_folder(session: AsyncSession, folder: Folder, new_parent: Folder):
        folder.parent = new_parent
        await session.commit()
        return folder


class FileService:
    @staticmethod
    async def get(session: AsyncSession, file_id):
        return await session.get(File, file_id, options=[selectinload(File.versions)])

    @staticmethod
    async def get_count_by_parent_and_name_contains(
        session: AsyncSession, parent_id: int, name: str
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(File)
            .where(File.parent_id == parent_id)
            .where(File.name.contains(name))
        )
        result = await session.scalar(stmt)

        return result or 0

    @staticmethod
    async def get_by_parent_and_name(
        session: AsyncSession, parent: Folder, name: str
    ) -> File:
        stmt = (
            select(File)
            .where(File.parent_id == parent.id)
            .where(File.name == name)
            .options(selectinload(File.versions))
        )
        result = await session.scalars(stmt)

        return result.first()

    @staticmethod
    async def create(
        session: AsyncSession, telegram_file_data: dict, parent: Folder
    ) -> File:

        if not telegram_file_data.get("name"):
            current_date = datetime.now()
            file_type = telegram_file_data["type"].split("/")[-1]
            name = f"{current_date.strftime('%Y-%m-%d_%H-%M-%S')}.{file_type}"

            count = await FileService.get_count_by_parent_and_name_contains(
                session, parent.id, name.split(".")[0]
            )

            if count > 0:
                name = (
                    f"{telegram_file_data["type"].split("/")[0]}_"
                    f"{name.split('.')[0]}_({count + 1}).{file_type}"
                )

            telegram_file_data["name"] = name

        first_version = FileVersion(
            version=1,
            telegram_file_id=telegram_file_data["telegram_file_id"],
            size=telegram_file_data["size"],
        )

        file = File(
            parent=parent,
            name=telegram_file_data["name"],
            type=telegram_file_data["type"],
            versions=[first_version],
            is_telegram_photo=telegram_file_data["is_telegram_photo"],
        )
        session.add(file)
        await session.commit()
        await session.refresh(file)
        return file

    @staticmethod
    async def create_new_version(
        session: AsyncSession, file: File, update_data: dict
    ) -> File:
        file.versions.append(
            FileVersion(
                version=file.versions[-1].version + 1,
                telegram_file_id=update_data["telegram_file_id"],
                size=update_data["size"],
            )
        )
        session.add(file)
        await session.commit()
        return file

    @staticmethod
    async def update_or_create(
        session: AsyncSession, telegram_file_data: dict, parent: Folder
    ) -> Tuple[str, File]:
        file = None
        if telegram_file_data["name"]:
            file = await FileService.get_by_parent_and_name(
                session, parent, telegram_file_data["name"]
            )

        if file:
            return "updated", await FileService.create_new_version(
                session, file, telegram_file_data
            )

        return "created", await FileService.create(session, telegram_file_data, parent)

    @staticmethod
    async def update(session: AsyncSession, file_update_in: FileUpdate, file: File):
        for key, value in file_update_in.model_dump().items():
            setattr(file, key, value)

        await session.commit()
        return file

    @staticmethod
    async def delete(
        session: AsyncSession,
        file: File,
    ):
        await session.delete(file)
        await session.commit()

    @staticmethod
    async def move(
        session: AsyncSession,
        file: File,
        new_parent_id: int,
    ):
        file.parent_id = new_parent_id
        await session.commit()

    @staticmethod
    async def get_version(file: File, version: int, session: AsyncSession):
        if version < 0:
            return None

        try:
            await session.refresh(file)
            return file.versions[version - 1]
        except IndexError:
            return None
