from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
from bson import ObjectId

from datetime import datetime
from typing import Sequence, Any, Mapping

from config import mongo_settings


class MongoService:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(f"mongodb://{mongo_settings.user}:{mongo_settings.password}@{mongo_settings.host}:{mongo_settings.port}")
        self.db = self.client[mongo_settings.db]

    async def insert(self, collection: str, document: Mapping[str, Any]) -> str:
        collection = self.db[collection]
        document["created_at"] = str(datetime.now())
        result = await collection.insert_one(document)
        return result.inserted_id

    async def get(
        self, collection: str, query: Mapping[str, Any] = {}
    ) -> Sequence[Mapping[str, Any]]:
        collection = self.db[collection]
        cursor = collection.find(query)
        documents = await cursor.to_list(length=None)

        result = []
        for doc in documents:
            doc_dict = dict(doc)
            if "_id" in doc_dict:
                doc_dict["_id"] = str(doc_dict["_id"])
            result.append(doc_dict)

        return result

    async def insert_many(
        self, collection: str, documents: Sequence[Mapping[str, Any]]
    ) -> Sequence[str]:
        collection = self.db[collection]
        for doc in documents:
            doc["created_at"] = str(datetime.now())
            doc["likes"] = 0
            doc["dislikes"] = 0
        result = await collection.insert_many(documents)
        return result.inserted_ids

    async def add_like(self, collection: str, document_id: str, user_id: str) -> bool:
        vote_exists = await self.db["votes"].find_one(
            {"document_id": ObjectId(document_id), "user_id": user_id}
        )
        if vote_exists:
            return False
        try:
            await self.db["votes"].insert_one(
                {
                    "document_id": ObjectId(document_id),
                    "user_id": user_id,
                    "type": "like",
                    "created_at": str(datetime.now()),
                }
            )
        except DuplicateKeyError:
            return False

        result = await self.db[collection].update_one(
            {"_id": ObjectId(document_id)}, {"$inc": {"likes": 1}}
        )
        return result.modified_count > 0

    async def add_dislike(self, collection: str, document_id: str, user_id: str) -> bool:
        vote_exists = await self.db["votes"].find_one(
            {"document_id": ObjectId(document_id), "user_id": user_id}
        )
        if vote_exists:
            return False

        try:
            await self.db["votes"].insert_one(
                {
                    "document_id": ObjectId(document_id),
                    "user_id": user_id,
                    "type": "dislike",
                    "created_at": str(datetime.now()),
                }
            )
        except DuplicateKeyError:
            return False

        result = await self.db[collection].update_one(
            {"_id": ObjectId(document_id)}, {"$inc": {"dislikes": 1}}
        )
        return result.modified_count > 0

    async def get_collections(self) -> Sequence[str]:
        return await self.db.list_collection_names()

    async def create_collection(self, collection_name: str) -> bool:
        try:
            await self.db.create_collection(collection_name)
            return True
        except CollectionInvalid:
            return collection_name in await self.db.list_collection_names()
        except Exception as e:
            print(f"Error creating collection {collection_name}: {e}")
            return False
