from dependency_injector import containers, providers
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from apps.account.service import AccountService
from apps.scanner.service import BlockScanner
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.transaction.service import TransactionService
from core.config import ServerConfig
from core.producer import HttpProducer
from core.ton_provider import (
    TONAPIClientAsync,
)
from database.local_storage import RedisStorage


class CoreContainer(containers.DeclarativeContainer):
    config: ServerConfig = providers.Configuration(default=ServerConfig().dict())

    wiring_config = containers.WiringConfiguration(
        modules=[
            "apps.account.router",
            # "scanner.router",
        ]
    )

    engine = providers.Singleton(create_async_engine, config.database_uri, echo=False)
    async_session = providers.Factory(async_sessionmaker, engine, expire_on_commit=False)
    db = providers.Singleton(TonQuestSQLAlchemyRepo, async_session)

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

    account_service = providers.Factory(
        AccountService,
        transaction_service=providers.Factory(
            TransactionService,
            ton_rpc_client=ton_rpc_client,
        ),
        ton_rpc_client=ton_rpc_client,
        producer=producer,
        ton_quest_repository=db,
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
