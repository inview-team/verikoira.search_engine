import json

from rabbit.client import RabbitClient


class Worker:
    def __init__(self, config: dict):
        self._rabbit = RabbitClient(
            raw_rabbit_config=config,
            process_task_function=self.get_task_from_rabbit,
            consuming_queue_title="engine",
            consuming_queue_exchange="task"
        )
        self._rabbit.begin_consumption()

    @staticmethod
    def get_task_from_rabbit(data: str) -> dict:
        data = json.loads(data)
        print(data['payload'])
        return {'result':'ok'}
