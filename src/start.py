import os

from utils.logger.log import logger
from worker.worker import Worker
from utils import environments as env

if __name__ == '__main__':
    rabbit_config = {
        "ip": env.RABBIT,
        "port": env.RABBIT_PORT,
        "user": env.RABBIT_USER,
        "password": env.RABBIT_PASS,
        "exchangeTasks": "tasks",
        "exchangeAnswers": "results",
    }
    mongo_config = {
        "ip": env.MONGO,
        "port": env.MONGO_PORT,
        "user": env.MONGO_USER,
        "password": env.MONGO_PASS,
        "database": "storage",
    }
    try:
        worker = Worker(rabbit_config, mongo_config, env.SERVICE_TYPE)
    except Exception:
        logger.critical("Critical error during service work", exc_info=True)
        os._exit(1)