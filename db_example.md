```python
from DB.DB import DB
from DB.enums.BookStatus import BookStatus
from DB.TypedDict.BooksTypedDict import UserShelfBookTypedDict, BookInfoTypedDict

db = DB()

telegram_id = 123
book_id = 1
status = BookStatus.read

db.add_book_to_user_shelf(telegram_id, book_id, status) # добавить книгу в список

db.remove_book_from_shelf(telegram_id, book_id) # удалить книгу из списка

data = db.get_user_bookshelf(telegram_id) # получить полный список прочитанных книг
# Формат возвращаемых данных
data: list[UserShelfBookTypedDict]  = [
    {
        "book_id": 2,
        "litres_id": 456,
        "picture": "url",
        "author": "Автор",
        "name": "Название",
        "description": "Описание",
        "book_status": BookStatus.read
    }
]

data = db.search_book("Название") # поиск по точному названию книги

data: list[BookInfoTypedDict]  = [
    {
        "book_id": 2,
        "litres_id": 456,
        "picture": "url",
        "author": "Автор",
        "name": "Название",
        "description": "Описание"
    }
]
```