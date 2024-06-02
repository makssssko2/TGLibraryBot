from typing import TypedDict
from ..enums.BookStatus import BookStatus


class UserShelfBookTypedDict(TypedDict):
    book_id: int
    litres_id: int
    picture: str
    author: str
    name: str
    description: str
    book_status: BookStatus


class BookInfoTypedDict(TypedDict):
    book_id: int
    litres_id: int
    picture: str
    author: str
    name: str
    description: str
