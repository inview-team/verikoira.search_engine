from dataclasses import dataclass


@dataclass
class RabbitConfig:
    ip: str
    port: str
    user: str
    password: str
    exchangeTasks: str
    exchangeAnswers: str


@dataclass
class MongoConfig:
    ip: str
    port: str
    user: str
    password: str
    database: str
