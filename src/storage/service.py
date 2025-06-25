from datetime import datetime
from typing import Tuple

from sqlalchemy import select, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from storage.models import File, Folder, FileVersion
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

        await session.execute(text(query), {"folder_id": folder.id})
        await session.commit()

    @staticmethod
    async def update(
        session: AsyncSession, folder_update_in: FolderUpdate, folder: Folder
    ):
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

    # @staticmethod
    # async def copy_folder(session: AsyncSession, copy_folder, target_folder):
    #     source_folder_id = copy_folder.id
    #     new_parent_id = target_folder.id
    #     try:
    #         # 1. Копируем основную папку
    #         copy_folder_query = text("""
    #             INSERT INTO folder (name, parent_id, owner_id, is_root, path)
    #             SELECT
    #                 name || ' (copy)',
    #                 :new_parent_id,
    #                 owner_id,
    #                 is_root,
    #                 NULL
    #             FROM folder
    #             WHERE id = :source_folder_id
    #             RETURNING id
    #         """)
    #
    #         result = await session.execute(
    #             copy_folder_query,
    #             {"source_folder_id": source_folder_id,
    #              "new_parent_id": new_parent_id}
    #         )
    #         new_folder_id = result.scalar()
    #         await session.commit()
    #
    #         # 2. Получаем все вложенные папки рекурсивно
    #         get_subfolders_query = text("""
    #             WITH RECURSIVE folder_tree AS (
    #                 SELECT id, name, parent_id, owner_id, is_root
    #                 FROM folder
    #                 WHERE id = :source_folder_id
    #
    #                 UNION ALL
    #
    #                 SELECT f.id, f.name, f.parent_id, f.owner_id, f.is_root
    #                 FROM folder f
    #                 JOIN folder_tree ft ON f.parent_id = ft.id
    #             )
    #             SELECT * FROM folder_tree WHERE id != :source_folder_id
    #         """)
    #
    #         result = await session.execute(
    #             get_subfolders_query,
    #             {"source_folder_id": source_folder_id}
    #         )
    #         subfolders = result.fetchall()
    #
    #         folder_mappings = {source_folder_id: new_folder_id}
    #
    #         for folder in subfolders:
    #             old_id, name, parent_id, owner_id, is_root = folder
    #             new_parent_id = folder_mappings[parent_id]
    #
    #             insert_query = text("""
    #                 INSERT INTO folder (name, parent_id, owner_id, is_root, path)
    #                 VALUES (:name, :parent_id, :owner_id, :is_root, NULL)
    #                 RETURNING id
    #             """)
    #
    #             result = await session.execute(
    #                 insert_query,
    #                 {
    #                     "name": name,
    #                     "parent_id": new_parent_id,
    #                     "owner_id": owner_id,
    #                     "is_root": is_root
    #                 }
    #             )
    #             new_id = result.scalar()
    #             folder_mappings[old_id] = new_id
    #
    #         await session.commit()
    #
    #         if folder_mappings:
    #             file_mappings = {}
    #
    #             get_files_query = text("""
    #                 SELECT id, name, type, parent_id
    #                 FROM file
    #                 WHERE parent_id = ANY(:parent_ids)
    #             """)
    #
    #             result = await session.execute(
    #                 get_files_query,
    #                 {"parent_ids": list(folder_mappings.keys())}
    #             )
    #             files = result.fetchall()
    #
    #             for file_id, name, file_type, old_parent_id in files:
    #                 new_parent_id = folder_mappings[old_parent_id]
    #
    #                 insert_file_query = text("""
    #                     INSERT INTO file (name, type, parent_id, _path_cache)
    #                     VALUES (:name, :type, :parent_id, NULL)
    #                     RETURNING id
    #                 """)
    #
    #                 result = await session.execute(
    #                     insert_file_query,
    #                     {
    #                         "name": name,
    #                         "type": file_type,
    #                         "parent_id": new_parent_id
    #                     }
    #                 )
    #                 new_file_id = result.scalar()
    #                 file_mappings[file_id] = new_file_id
    #
    #             if file_mappings:
    #                 get_versions_query = text("""
    #                     SELECT created_at, version, telegram_file_id, file_id, size
    #                     FROM file_version
    #                     WHERE file_id = ANY(:file_ids)
    #                 """)
    #
    #                 result = await session.execute(
    #                     get_versions_query,
    #                     {"file_ids": list(file_mappings.keys())}
    #                 )
    #                 versions = result.fetchall()
    #
    #                 for created_at, version, telegram_file_id, old_file_id, size in versions:
    #                     new_file_id = file_mappings[old_file_id]
    #
    #                     insert_version_query = text("""
    #                         INSERT INTO file_version (created_at, version, telegram_file_id, file_id, size)
    #                         VALUES (:created_at, :version, :telegram_file_id, :file_id, :size)
    #                     """)
    #
    #                     await session.execute(
    #                         insert_version_query,
    #                         {
    #                             "created_at": created_at,
    #                             "version": version,
    #                             "telegram_file_id": telegram_file_id,
    #                             "file_id": new_file_id,
    #                             "size": size
    #                         }
    #                     )
    #
    #         for old_folder_id, new_folder_id in folder_mappings.items():
    #             copy_edit_access_query = text("""
    #                 INSERT INTO folder_editing_access (folder_id, user_id)
    #                 SELECT :new_folder_id, user_id
    #                 FROM folder_editing_access
    #                 WHERE folder_id = :old_folder_id
    #             """)
    #
    #             await session.execute(
    #                 copy_edit_access_query,
    #                 {"old_folder_id": old_folder_id,
    #                  "new_folder_id": new_folder_id}
    #             )
    #
    #             copy_view_access_query = text("""
    #                 INSERT INTO folder_view_access (folder_id, user_id)
    #                 SELECT :new_folder_id, user_id
    #                 FROM folder_view_access
    #                 WHERE folder_id = :old_folder_id
    #             """)
    #
    #             await session.execute(
    #                 copy_view_access_query,
    #                 {"old_folder_id": old_folder_id,
    #                  "new_folder_id": new_folder_id}
    #             )
    #
    #         await session.commit()
    #         return await FolderService.get(session, new_folder_id)
    #
    #     except Exception as e:
    #         await session.rollback()
    #         raise e


class FileService:
    @staticmethod
    async def get(session: AsyncSession, file_id):
        return await session.get(File, file_id)

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
        )
        session.add(file)
        await session.commit()
        await session.refresh(file)
        return file

    @staticmethod
    async def update(session: AsyncSession, file: File, update_data: dict) -> File:
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
            return "updated", await FileService.update(
                session, file, telegram_file_data
            )

        return "created", await FileService.create(session, telegram_file_data, parent)
