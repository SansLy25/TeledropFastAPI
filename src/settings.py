import secrets
from os import getenv

from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            host=self.POSTGRES_HOST,
            password=self.POSTGRES_PASSWORD,
            port=5432,
            path=f"/{self.POSTGRES_DB}",
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()