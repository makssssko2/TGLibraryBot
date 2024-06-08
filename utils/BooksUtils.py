from DB.TypedDict.BooksTypedDict import BookInfoTypedDict


class BooksUtils:
    @staticmethod
    def get_book_caption(books: BookInfoTypedDict) -> str:
        caption = ""
        caption += f'<b>{books["name"]}\n'
        caption += f'Автор: {books["author"]}\n\n'
        caption += f'Издание: {books["publisher"]}\n'
        caption += f'Год: {books["year"]}</b>' if books["year"] is not None and books["year"] != "None" else '</b>'
        caption += f'\n\n{books["description"]}'
        caption = BooksUtils.truncate_text(caption, 1020)

        return caption

    @staticmethod
    def truncate_text(text: str, max_length: int = 4096) -> str:
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text
