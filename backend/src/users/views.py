from fastapi import APIRouter

from users.auth import UserDp
from users.schemas import UserRead

user_rt = APIRouter(prefix="/users")


@user_rt.get("/me", tags=["Пользователи"])
async def get_me(user: UserDp) -> UserRead:
    return user
