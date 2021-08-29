from pymongo import MongoClient

from ..structures import MongoConfig
from utils.logger.log import logger


class MongoInteraction:
    def __init__(self, config: MongoConfig):
        self._client = MongoClient(
            host=[f"{config.ip}:{config.port}"],
            username=config.user,
            password=config.password
        )
        logger.info(f"Server version: {self._client.server_info()['version']}")
        self._db = self._client[config.database]
        self._collection = None

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, collection):
        self._collection = self._db[collection]

    def add_values_to_collection(self, data: list) -> int:
        amount_inserted_documents = 0
        for value in data:
            if self.is_value_exist(title=value["title"]):
                continue
            amount_inserted_documents += 1
            self._collection.insert_one(value)
        logger.info(
            f"Inserted {amount_inserted_documents} new patents into collection."
        )
        return amount_inserted_documents

    def is_value_exist(self, title: str) -> bool:
        return self._collection.find_one({"title": title}) is not None

    def get_list_of_uploaded_values(self) -> list[int]:
        documents = self._collection.find({})
        return [document["_id"] for document in documents]
