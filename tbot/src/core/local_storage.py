from abc import ABC, abstractmethod
from typing import Type

from redis.asyncio.client import Redis


class LocalStorage(ABC):
    @abstractmethod
    def get_aiogram_local_storage(self) -> int | None:
        pass


class RedisLocalStorage(LocalStorage):
    def __init__(self, redis: Type[Redis], connect_url: str):
        self.redis = redis.from_url(connect_url)

    def get_aiogram_local_storage(self) -> Redis:
        return self.redis
