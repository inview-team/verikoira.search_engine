from pymongo import MongoClient

from mongo.structures import MongoConfig
from logger.log import logger


class MongoInteraction:
    def __init__(self, config: MongoConfig):
        self._client = MongoClient(
            host=f"{config.ip}:{config.port}",
            serverSelectionTimeoutMS=3000,
            username=config.user,
            password=config.password,
            authSource=config.database,
        )
        logger.info(f"Server version: {self._client.server_info()['version']}")
        self._db = self._client[config.database]
        self._collection = self._db['patents']

    def add_values_to_collection(self, data: list) -> int:
        amount_inserted_documents = 0
        for value in data:
            if self.is_value_exist(title=value["title"]):
                continue
            amount_inserted_documents += 1
            self._collection.insert_one(value)
        logger.info(f"Inserted {amount_inserted_documents} new patents into collection.")
        return amount_inserted_documents

    def is_value_exist(self, title: str) -> bool:
        return self._collection.find_one({"title": title}) is not None

    def get_list_of_uploaded_values(self) -> list[int]:
        documents = self._collection.find({})
        return [document["_id"] for document in documents]
