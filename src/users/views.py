from fastapi import APIRouter

from users.auth import UserDp
from users.schemas import UserRead

user_rt = APIRouter(prefix="/users")


@user_rt.post("/me", response_model=UserRead, tags=["Users"])
async def get_me(user: UserDp):
    return user
