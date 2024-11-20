from abc import ABC, abstractmethod
from typing import Type

from redis.asyncio.client import Redis


class LocalStorage(ABC):
    service = None

    @abstractmethod
    async def get_last_scanned_block(self) -> int | None:
        pass

    @abstractmethod
    async def set_last_scanned_block(self, block_number: int) -> None:
        pass

    @abstractmethod
    async def reset_last_scanned_block(self) -> None:
        pass


class RedisStorage(LocalStorage):
    service = "TON_SERVICE"

    def __init__(self, redis: Type[Redis], connect_url: str):
        self.redis = redis.from_url(connect_url)

    async def get_last_scanned_block(self) -> int | None:
        last_block = await self.redis.get(f"{self.service}:last_scanned_block")
        return int(last_block) if last_block else None

    async def set_last_scanned_block(self, block: int) -> None:
        await self.redis.set(f"{self.service}:last_scanned_block", str(block))
        return

    async def reset_last_scanned_block(self) -> None:
        await self.redis.delete(f"{self.service}:last_scanned_block")
        return
