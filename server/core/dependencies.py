from dependency_injector import containers, providers
from redis.asyncio.client import Redis

from apps.account.repositories import MongoDBAccountRepository
from apps.account.service import AccountService
from apps.scanner.service import BlockScanner
from apps.transaction.service import TransactionService
from core.config import ServerConfig
from core.producer import HttpProducer
from core.ton_provider import (
    TONAPIClientAsync,
)
from database.engine import get_async_mongo_engine
from database.local_storage import RedisStorage


class CoreContainer(containers.DeclarativeContainer):
    config: ServerConfig = providers.Configuration(default=ServerConfig().dict())

    wiring_config = containers.WiringConfiguration(
        modules=[
            "apps.account.router",
            # "scanner.router",
        ]
    )

    local_storage = providers.ThreadLocalSingleton(
        RedisStorage, Redis, connect_url=config.redis_url
    )

    ton_rpc_client = providers.Factory(
        TONAPIClientAsync, base_url=config.ton_rpc_url, key=config.rpc_api_key
    )

    producer = providers.Factory(
        HttpProducer,
        base_url=config.backend_url,
    )

    mongo_engine = providers.Singleton(
        get_async_mongo_engine,
        mongo_conn=config.database_uri,
        mongo_db=config.database_name,
    )

    account_repository = providers.Factory(
        MongoDBAccountRepository,
        mongo_engine,
    )
    transaction_repository = providers.Factory(
        MongoDBAccountRepository,
        mongo_engine,
    )
    transaction_service = providers.Factory(
        TransactionService,
        repository=transaction_repository,
        ton_rpc_client=ton_rpc_client,
    )

    account_service = providers.Factory(
        AccountService,
        repository=account_repository,
        ton_rpc_client=ton_rpc_client,
        transaction_service=transaction_service,
        producer=producer,
    )

    scanner_service = providers.Singleton(
        BlockScanner,
        local_storage=local_storage,
        ton_rpc_client=ton_rpc_client,
        account_service=account_service,
    )


async def initialize_container(container: CoreContainer) -> None:
    config = ServerConfig()
    container.config = config
    container.init_resources()
