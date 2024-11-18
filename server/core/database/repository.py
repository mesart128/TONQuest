from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id_: str):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all_by(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: str, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id_: str):
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    collection_name = None

    def __init__(self, motor_db: AsyncIOMotorDatabase):
        self._motor_db = motor_db
        self._collection = motor_db[self.collection_name]

    async def add_one(self, data: Dict[str, Any]) -> str:
        result = await self._collection.insert_one(data)
        return str(result.inserted_id)

    async def delete_one(self, id_: str) -> int:
        result = await self._collection.delete_one({"_id": ObjectId(id_)})
        return result.deleted_count

    async def edit_one(self, id_: str, data: Dict[str, Any]) -> int:
        result = await self._collection.update_one({"_id": ObjectId(id_)}, {"$set": data})
        return result.modified_count

    async def find_all(self) -> list:
        cursor = self._collection.find()
        result = await cursor.to_list(length=None)
        return [{**doc, "_id": str(doc["_id"])} for doc in result]

    async def find_one(self, id_: str) -> Optional[dict]:
        doc = await self._collection.find_one({"_id": ObjectId(id_)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def find_one_by(self, **kwargs) -> Optional[dict]:
        doc = await self._collection.find_one(kwargs)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def find_all_by(self, **kwargs) -> list:
        cursor = self._collection.find(kwargs).sort("created_at", -1)
        result = await cursor.to_list(length=None)
        return [{**doc, "_id": str(doc["_id"])} for doc in result]

    async def commit(self):
        # MongoDB is usually auto-commit, so this is a placeholder.
        pass
