from abc import ABC

from core.database.repository import AbstractRepository, MongoDBRepository


class BaseAccountRepository(AbstractRepository, ABC):
    pass


class MongoDBAccountRepository(MongoDBRepository, BaseAccountRepository):
    collection_name = "accounts"
