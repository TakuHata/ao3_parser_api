from typing import TypedDict, Optional

class FicData(TypedDict):
    title: str
    author: str
    fandom: str
    datetime: str
    tags: str
    summary: str
    language: str
    words: int
    chapters_current: int
    chapters_total: Optional[int]
    comments: int
    kudos: int
    hits: int
    url: str