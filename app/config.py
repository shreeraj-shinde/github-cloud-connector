from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int = None
    DATABASE_URL: str = ""
    APP_ENV: str = "development"
    GIT_CLIENT_ID: str = ""
    GIT_CLIENT_SECRET: str = ""
    SECRET: str = ""
    ALGORITHM: str = ""
    CORS_ORIGINS: str = ""
    TOKEN_EXPIRE_HOURS: int = None
    PERSONAL_ACCESS_TOKEN : str = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
