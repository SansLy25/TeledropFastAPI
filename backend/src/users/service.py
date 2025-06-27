from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from telegram_webapp_auth.data import WebAppUser

from storage.models import Folder
from users.models import User
from users.schemas import UserCreate


class UserService:
    @staticmethod
    async def get(*, session: AsyncSession, user_id: int) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def get_by_tg_id(*, session: AsyncSession, tg_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.telegram_id == tg_id)
            .options(
                selectinload(User.current_folder), selectinload(User.all_owned_folders)
            )
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def create(*, session: AsyncSession, user_in: WebAppUser) -> User:
        telegram_id = user_in.id
        user_data = user_in.__dict__

        del user_data["id"]

        for key in user_data:
            if user_data[key] == "":
                user_data[key] = None

        user = User(
            **UserCreate.model_validate(
                {**user_data, "telegram_id": telegram_id}
            ).model_dump()
        )
        root_folder = Folder(name="", owner=user, is_root=True)

        session.add_all([user, root_folder])
        await session.commit()
        return user
