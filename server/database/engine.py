from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from core.config import base_config, ServerConfig
from database.utils import ThreadMongoSingleton


def get_async_mongo_engine(mongo_conn: str, mongo_db: str) -> ThreadMongoSingleton:
    return ThreadMongoSingleton(
        mongo_conn=mongo_conn,
        mongo_db=mongo_db,
    )


async_engine = create_async_engine(base_config.database_uri, echo=False)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


engine = create_async_engine(base_config.database_uri, echo=False)
async_session = async_sessionmaker(
    engine, expire_on_commit=False
)
db = TonQuestSQLAlchemyRepo(async_session)
