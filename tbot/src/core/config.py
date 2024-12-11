import contextvars
import pathlib
from typing import Literal
from uuid import uuid4

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = pathlib.Path(__file__).parent.parent.parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

REQ_ID_CONTEXT = contextvars.ContextVar("context_id", default=str(uuid4()))

ASYNC_LOCK_KEY = "aio_async_lock"


class TelegramConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env", env_file_encoding="utf-8", extra="allow"
    )
    SETTINGS_MODULE: Literal["DEV", "PROD"] = "DEV"
    BOT_TOKEN: str
    BOT_NICKNAME: str
    REDIS_URL: str
    WEB_APP_URL: str
    CHANNEL_URL: str

    # bot moderator
    # CHANNEL_URL: str
    # CHANNEL_NAME: str
    # CHAT_ID: str
    ADMIN_ID: int


# class MongoConfig(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=PROJECT_DIR / ".env", env_file_encoding="utf-8", extra="allow"
#     )
#     mongo_db_url: str
#     mongo_db_name: str = "needify_tbot"


class Config(BaseSettings):
    telegram: TelegramConfig


def load_config() -> Config:
    return Config(telegram=TelegramConfig())


env_config = load_config()
