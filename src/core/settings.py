from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Db(BaseModel):
    url: PostgresDsn
    pool_size: int = 30
    max_overflow: int = 10
    echo: bool = True
    echo_pool: bool = True

    naming_convection: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class RunApp(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8082
    reload: bool = True
    app: str = "main:app"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env_template", BASE_DIR / ".env"),
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        case_sensitive=False,
    )

    db: Db
    api: ApiPrefix = ApiPrefix()
    app: RunApp = RunApp()


settings = Settings()
