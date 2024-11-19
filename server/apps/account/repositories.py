from abc import ABC

from database.repository import AbstractRepository, MongoDBRepository


class BaseAccountRepository(AbstractRepository, ABC):
    pass


class MongoDBAccountRepository(MongoDBRepository, BaseAccountRepository):
    collection_name = "accounts"
