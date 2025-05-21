from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    telegram_id: int = Field(unique=True)
    telegram_username: int

