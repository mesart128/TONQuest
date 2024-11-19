import asyncio
import logging
import os
import sys

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.dependencies import (  # noqa: E402
    CoreContainer,
    initialize_container,
)
from core.logger import setup_logging  # noqa: E402

setup_logging()


async def runner(restart: bool = False):
    _container = CoreContainer()
    try:
        await initialize_container(_container)
        if restart is False and _container.config.update_last_scanned_block is True:
            logging.info("Resetting last scanned block")
            local_storage = _container.local_storage()
            await local_storage.reset_last_scanned_block()
        scanner = _container.scanner_service()
        await scanner.run()
    except Exception as e:
        logging.error(f"Error in scanner {type(e)}: {e}", exc_info=True)
        await asyncio.sleep(10)
        return await runner(True)


if __name__ == "__main__":
    asyncio.run(runner())
