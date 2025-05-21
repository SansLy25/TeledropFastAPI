from fastapi import APIRouter


user_rt = APIRouter(prefix="/users")


@user_rt.post("/me")
async def login():
    pass
