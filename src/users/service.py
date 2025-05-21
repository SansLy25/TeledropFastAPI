from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class UserService:
    @staticmethod
    async def get(*, session: AsyncSession, user_id: int) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def create(
            *,
            session: AsyncSession,
            username: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            telegram_id: int,
            telegram_username
    ):
        try:
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                telegram_id=telegram_id,
                telegram_username=telegram_username
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Пользователь с таким id уже существует"
            )

        session.add(user)
        await session.commit()
        return user
