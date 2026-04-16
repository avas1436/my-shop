from enum import Enum
from functools import lru_cache
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# خواندن نام محیط از سیستم عامل
env_state = os.getenv("env", "dev")
env_file_name = f".env.{env_state}" if env_state != "dev" else ".env"


class Environment(str, Enum):
    development = "dev"
    production = "prod"


class Settings(BaseSettings):
    # app name ans version
    app_name: str = "Shop Backend"
    app_version: str = "1.0.0"

    # environment of running app
    environment: Environment = Field(
        default=Environment.development, description="محیط اجرای توسعه یا محصول نهایی"
    )

    debug: bool = False
    log_level: str = Field(default="INFO")
    timezone: str = Field(default="UTC")
    secret_key: str = Field(
        default="change-me", min_length=8, description="کلید محرمانه پروژه"
    )

    # development urls
    docs_enable: bool = True
    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"
    redoc_url: str = "redoc"
    api_v1_prefix: str = "/api/v1"

    # cors middleware
    cors_origins: list[str] = ["https://myapp.com"]
    cors_allow_methods: list[str] = ["GET", "POST", "OPTIONS"]
    cors_allow_headers: list[str] = ["Authorization", "Content-Type"]
    cors_expose_headers: list[str] = ["X-Request-ID"]
    cors_allow_credentials: bool = True
    cors_max_age: int = 600  # کش مرورگر

    # trusted_hosts
    trusted_hosts: list[str] = Field(default=["localhost", "127.0.0.1"])

    # database settings
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/shop"
    )
    sql_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 15
    db_pool_recycle: int = 1800
    db_pool_pre_ping: bool = True

    # redis settings
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 10
    redis_socket_timeout: int = 5
    session_prefix: str = "session"

    # jwt config
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=env_file_name,
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
