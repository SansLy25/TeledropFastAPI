from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(unique=True)
    username: Optional[str] = None
    language_code: Optional[str] = None
    photo_url: Optional[str] = None



