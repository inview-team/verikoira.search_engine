import abc


class Robot(abc.ABC):
    @abc.abstractmethod
    def produce_search_query(self, id: str, keyword: str) -> None:
        """Find information by keyword

        Args:
            id: id of task
            keyword (str): keyword for searching

        Returns:
            None
        """
