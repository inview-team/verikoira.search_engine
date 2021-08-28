from dataclasses import dataclass


@dataclass
class PatentInfo:
    title: str
    authors: list[str]
    patent_owner: str
    referat: str