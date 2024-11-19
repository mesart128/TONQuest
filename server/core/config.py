import contextvars
import pathlib
from typing import Literal, Optional, Union
from uuid import uuid4

from pydantic import RedisDsn
from pydantic_settings import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.parent
PROJECT_DIR = BASE_DIR / "src"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

CONTEXT_ID = contextvars.ContextVar("context_id", default=str(uuid4()))


class ServerConfig(BaseSettings):
    database_uri: str
    database_name: str  # for mongo
    redis_url: Union[str, RedisDsn]
    hot_wallet_mnemonic: str  # 24 words
    update_last_scanned_block: bool = False
    ton_rpc_url: Optional[str] = (
        "https://go.getblock.io/95dfd73af9144e4e823cc81f2bed942a"  # free tier
    )
    rpc_api_key: Optional[str] = None
    backend_url: Optional[str] = None

    class Config:
        extra = "ignore"
        env_file = ".env"
        protected_namespaces = ("model_",)

    @property
    def hd_wallet_mnemonic_list(self):
        return self.hot_wallet_mnemonic.split()


class LoggerSettings(BaseSettings):
    settings_module: Literal["DEV", "PROD"] = "DEV"
    graylog_host: Optional[str] = "localhost"
    graylog_port: Union[int, str] = 12201

    class Config:
        env_file = ".env"
        extra = "allow"
        protected_namespaces = ("model_",)


base_config = ServerConfig()
