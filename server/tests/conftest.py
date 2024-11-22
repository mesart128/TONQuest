# flake8: noqa
import os
import sys

import pytest
import pytest_asyncio
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.logger import setup_logging

setup_logging()
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from database.base import Base
from database.initial_data import populate_database


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.
    :return: backend name
    """
    return "asyncio"


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def database_engine(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password
    janitor = DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        password=pg_password,
        version=test_db.version,
    )
    janitor.init()

    connection_str = f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_async_engine(connection_str, echo=False)

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    await init_db()
    yield engine
    await engine.dispose()
    janitor.drop()


@pytest.fixture(scope="session")
def ton_quest_repo(database_engine):
    SessionFactory = async_sessionmaker(database_engine)
    return TonQuestSQLAlchemyRepo(SessionFactory)


@pytest_asyncio.fixture(scope="function")
async def setup_database(database_engine, ton_quest_repo):
    await populate_database(database_engine, ton_quest_repo)
