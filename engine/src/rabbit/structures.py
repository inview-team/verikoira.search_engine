from dataclasses import dataclass


@dataclass
class ClientConfig:
    ip: str
    port: int
    user: str
    password: str
    exchangeAnswers: str