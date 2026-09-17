import os
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
ENV_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    DATABASE_URL: str

    # ИСПРАВЛЕНО: добавлен параметр extra='ignore'
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')

setting = Settings()