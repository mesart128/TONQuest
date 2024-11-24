from abc import ABC

from database.repository import AbstractRepository, MongoDBRepository


class BaseTransactionRepository(AbstractRepository, ABC):
    pass


class TransactionMongoRepository(MongoDBRepository, BaseTransactionRepository):
    collection_name = "transactions"
