from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    open_meteo_url: str
    open_meteo_forecast_url: str
    open_meteo_archive_url: str
    database_url: str
    rabbitmq_url: str
    redis_url: str = "redis://redis:6379/0"
    reports_dir: str = "/var/lib/weather-reports"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
