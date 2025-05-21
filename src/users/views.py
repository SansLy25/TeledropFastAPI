from fastapi import APIRouter


user_rt = APIRouter(prefix="/users/")


@user_rt.post("/login")
async def login():
    pass
