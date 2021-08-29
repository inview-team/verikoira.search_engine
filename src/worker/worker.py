import json

from utils.rabbit.client import RabbitClient
from scrapper import robot_factory


class Worker:
    def __init__(self, rabbit_config: dict, mongo_config: dict, search_type: str):
        self._robot = robot_factory.get_robot(
            search_type,
            config=mongo_config,
        )
        self._rabbit = RabbitClient(
            raw_rabbit_config=rabbit_config,
            worker_type="patents",
            process_task_function=self.get_task_from_rabbit,
            consuming_queue_title="engine",
            consuming_routing_key="engine",
        )
        self._rabbit.begin_consumption()

    def get_task_from_rabbit(self, data: str):
        data = json.loads(data)
        task_id = data["task_id"]
        search_query = data["payload"]
        self._robot.produce_search_query(search_query)
        return {"id": task_id, "result": "ok"}

