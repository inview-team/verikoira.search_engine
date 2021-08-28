from yandex_patents.robot import Searcher
from mongo.structures import MongoConfig
from utils import environments as env

if __name__ == '__main__':
    config = MongoConfig(
        ip=env.MONGO,
        port=env.MONGO_PORT,
        user=env.MONGO_USER,
        password=env.MONGO_PASS,
        database=env.MONGO_DB
    )
    search = Searcher(config)
    search.find_information_by_keyword(env.KEYWORD)
