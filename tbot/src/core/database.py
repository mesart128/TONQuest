from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.core.config import env_config
from src.core.local_storage import RedisLocalStorage
from src.utils.database import ThreadMongoSingleton
local_storage = RedisLocalStorage(Redis, env_config.telegram.REDIS_URL)

redis_storage = RedisStorage(local_storage.get_aiogram_local_storage())

async_mongo = ThreadMongoSingleton(env_config.mongo.mongo_db_url, env_config.mongo.mongo_db_name)
