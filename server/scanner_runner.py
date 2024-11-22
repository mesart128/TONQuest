import asyncio
import logging
import os
import sys

from dotenv import find_dotenv, load_dotenv
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from apps.account.service import AccountService
from apps.scanner.service import BlockScanner
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.transaction.service import TransactionService
from core.config import base_config
from core.ton_provider import TONAPIClientAsync
from database.local_storage import RedisStorage

load_dotenv(find_dotenv())
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.logger import setup_logging  # noqa: E402

setup_logging()


async def runner(restart: bool = False):
    try:
        engine = create_async_engine(base_config.database_uri, echo=False)
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        db = TonQuestSQLAlchemyRepo(async_session)
        local_storage = RedisStorage(Redis, connect_url=base_config.redis_url)
        ton_rpc_client = TONAPIClientAsync(
            base_url=base_config.ton_rpc_url, keys=base_config.rpc_api_keys_list
        )
        account_service = AccountService(
            transaction_service=TransactionService(
                ton_rpc_client=ton_rpc_client,
            ),
            ton_rpc_client=ton_rpc_client,
            ton_quest_repository=db,
        )
        scanner_service = BlockScanner(
            local_storage=local_storage,
            ton_rpc_client=ton_rpc_client,
            account_service=account_service,
        )
        if restart is False and base_config.update_last_scanned_block is True:
            logging.info("Resetting last scanned block")
            await local_storage.reset_last_scanned_block()
        scanner = scanner_service
        await scanner.run()
    except Exception as e:
        logging.error(f"Error in scanner {type(e)}: {e}", exc_info=True)
        await asyncio.sleep(5)
        return await runner(True)


if __name__ == "__main__":
    asyncio.run(runner())
