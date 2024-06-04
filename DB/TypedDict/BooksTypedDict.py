from typing import TypedDict


class BookInfoTypedDict(TypedDict):
    book_id: int
    litres_id: int
    picture: str
    author: str
    name: str
    publisher: str
    description: str
    year: str
