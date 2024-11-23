import threading

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


class ThreadMongoSingleton:
    """
    This custom mongo class is needed to avoid errors when using asyncio logic with celery.
    We use threading local
    singleton to make sure that the same instance is used in the same thread. Otherwise, we
     will get an error
    "RuntimeError: Event loop is closed" or "Future attached to a different loop". To save
    backward compatibility,
    we provide access to database with __call__ method which return a new thread local
     singleton instance.
    For example:
        async_mongo = ThreadMongoSingleton(settings.mongo_conn, settings.mongo_db, sync_mode=False)

        async_mongo().chain_settings.find_one() # This will work
        async_mongo.chain_settings.find_one() # This will work too

    """

    def __init__(self, mongo_conn: str, mongo_db: str, sync_mode: bool = False):
        self._mongo_conn = mongo_conn
        self._mongo_db = mongo_db
        self._sync_mode = sync_mode

        self.__container = threading.local()
        self._get_database()

    def _factory(self):
        if self._sync_mode is True:
            return MongoClient(self._mongo_conn)[self._mongo_db]
        else:
            return AsyncIOMotorClient(self._mongo_conn)[self._mongo_db]

    def _get_database(self):
        if not hasattr(self.__container, "instance"):
            self.__container.instance = self._factory()
        return self.__container.instance

    def __getitem__(self, item):
        return self._get_database()[item]

    def __getattr__(self, item):
        return getattr(self._get_database(), item)

    def __call__(self, *args, **kwargs):
        return self._get_database()
