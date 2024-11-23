from src.core.database import async_mongo


class BaseUserDatabase:
    pass


class MongoUserDatabase(BaseUserDatabase):
    def __init__(self):
        self.async_mongo = async_mongo
        self.collection = self.async_mongo().users

    async def get_user(self, chat_id: int) -> dict | None:
        user = await self.collection.find_one({"chat_id": chat_id})
        return user

    async def add_user(self, user: dict):
        await self.collection.insert_one(user)

    async def update_user(self, chat_id: int, dict_to_update: dict):
        await self.collection.update_one({"user_id": chat_id}, {"$set": dict_to_update})
        return await self.get_user(chat_id)


def get_user_database() -> MongoUserDatabase:
    return MongoUserDatabase()
