from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBaseSchema):
    telegram_id: int
    username: Optional[str] = None
    language_code: Optional[str] = None
    photo_url: Optional[str] = None


class UserRead(UserCreate):
    id: int
