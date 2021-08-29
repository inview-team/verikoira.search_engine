import abc

from utils.mongo.mongo import MongoInteraction
from utils.structures import MongoConfig


class Robot(abc.ABC):
    def __init__(
            self,
            raw_mongo_config: dict
    ):
        config = MongoConfig(**raw_mongo_config)
        self._mongo_client = MongoInteraction(config)

    @abc.abstractmethod
    def produce_search_query(self, id: str, keyword: str) -> None:
        """Find information by keyword

        Args:
            id: id of task
            keyword (str): keyword for searching

        Returns:
            None
        """
