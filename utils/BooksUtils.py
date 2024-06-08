from DB.TypedDict.BooksTypedDict import BookInfoTypedDict


class BooksUtils:
    @staticmethod
    def get_book_caption(books: list[BookInfoTypedDict], index: int) -> str:
        caption = ""
        caption += f'<b>{books[index]["name"]}\n'
        caption += f'Автор: {books[index]["author"]}\n\n'
        caption += f'Издание: {books[index]["publisher"]}\n'
        caption += f'Год: {books[index]["year"]}</b>' if books[index]["year"] is not None else ''
        caption += f'\n\n{books[index]["description"]}'

        return caption
