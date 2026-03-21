from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Real-Time Batch Processing System"
    api_v1_prefix: str = "/"
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@db:5432/batch_processing")
    celery_broker_url: str = Field(default="redis://redis:6379/0")
    celery_result_backend: str = Field(default="redis://redis:6379/1")
    cors_origins: list[str] = ["http://localhost:3000"]
    upload_dir: str = "storage/uploads"
    batch_size: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
