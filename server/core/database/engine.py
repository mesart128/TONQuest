from core.database.utils import ThreadMongoSingleton


def get_async_mongo_engine(mongo_conn: str, mongo_db: str) -> ThreadMongoSingleton:
    return ThreadMongoSingleton(
        mongo_conn=mongo_conn,
        mongo_db=mongo_db,
    )
