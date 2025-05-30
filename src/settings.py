import secrets

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    TELEGRAM_BOT_TOKEN: str
    HOST_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.POSTGRES_HOST,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                port=5432,
                path=f"{self.POSTGRES_DB}",
            )
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
