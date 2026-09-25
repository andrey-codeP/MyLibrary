import os
from pathlib import Path
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    JWT_SECRET_TOKEN: str

    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def DATABASE_URL_STR(self) -> str:
        """Конвертирует PostgresDsn в строку для SQLAlchemy"""
        return str(self.DATABASE_URL)


# Создаем глобальный объект настроек
settings = Settings()
