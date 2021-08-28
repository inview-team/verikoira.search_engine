from dataclasses import dataclass


@dataclass
class MongoConfig:
    ip: str
    port: str
    user: str
    password: str
    database: str
