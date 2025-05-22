from typing import Any

from fastapi import APIRouter

from users.auth import UserDp

user_rt = APIRouter(prefix="/users")


@user_rt.post("/me")
async def login(user: UserDp):
    return user
