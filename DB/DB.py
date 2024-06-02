from typing import List, Type
from sqlalchemy import create_engine, text, func, Table, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker
from .enums.BookStatus import BookStatus
from .models import Base, Books, Users, UserShelf, UserRate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from .TypedDict.BooksTypedDict import UserShelfBookTypedDict, BookInfoTypedDict


class DB:

    def __init__(self):
        self.__engine = create_engine('sqlite:///AI.db')
        Base.metadata.create_all(self.__engine)
        self.__sessionmaker = sessionmaker(bind=self.__engine)

    def add_book(
            self,
            litres_id: int,
            url: str,
            picture: str,
            author: str,
            name: str,
            publisher: str,
            series: str,
            year: int,
            ISBN: str,
            description: str,
            age: int,
            lang: str,
            litres_isbn: str,
            genres: str
    ) -> None:
        with self.__sessionmaker() as session:
            book = Books(
                litres_id=litres_id,
                url=url,
                picture=picture,
                author=author,
                name=name,
                publisher=publisher,
                series=series,
                year=year,
                ISBN=ISBN,
                description=description,
                age=age,
                lang=lang,
                litres_isbn=litres_isbn,
                genres=genres
            )
            session.add(book)
            session.commit()

    def get_books(self) -> list[Type[Books]]:
        with self.__sessionmaker() as session:
            books = session.query(Books).all()
            return books

    def add_book_to_user_shelf(
            self,
            telegram_id: int,
            book_id: int,
            book_status: BookStatus
    ) -> bool:
        """Добавляет книгу в полку пользователя.
           Если пользователя нет в базе данных, то он создаётся.
           Если книга уже есть у пользователя, то возвращается False.

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги.
            book_status: Статус книги (например, "reading", "completed").

        Returns:
            True, если книга успешно добавлена, False в противном случае.
        """

        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    user = Users(telegram_id=telegram_id)
                    session.add(user)
                    session.commit()

                # Проверяем, есть ли уже эта книга у пользователя
                existing_item = session.query(UserShelf).filter_by(
                    user_id=user.id, book_id=book_id
                ).first()

                if existing_item:
                    return False  # Книга уже есть на полке

                new_shelf_item = UserShelf(
                    user_id=user.id, book_id=book_id, book_status=book_status
                )
                session.add(new_shelf_item)
                session.commit()
                return True

            except IntegrityError:
                session.rollback()
                return False

    def get_user_bookshelf(self, telegram_id: int) -> list[UserShelfBookTypedDict]:
        """Возвращает список книг на полке пользователя по его telegram_id.

        Args:
            telegram_id: Telegram ID пользователя.

        Returns:
            Список UserShelfBookTypedDict.
        """

        with self.__sessionmaker() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()

            if not user:
                user = Users(telegram_id=telegram_id)
                session.add(user)
                session.commit()

            bookshelf_items = (
                session.query(UserShelf)
                .options(joinedload(UserShelf.book))
                .filter(UserShelf.user_id == user.id)
                .all()
            )

            books: list[UserShelfBookTypedDict] = [
                {
                    "book_id": item.book.id,
                    "litres_id": item.book.litres_id,
                    "picture": item.book.picture,
                    "description": item.book.description,
                    "author": item.book.author,
                    "name": item.book.name,
                    "book_status": item.book_status.value
                }
                for item in bookshelf_items
            ]

            return books

    def update_book_status(
            self,
            telegram_id: int,
            book_id: int,
            new_status: BookStatus
    ) -> bool:
        """Обновляет статус книги в UserShelf.

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги.
            new_status: Новый статус книги.

        Returns:
            True, если статус успешно обновлён, False в противном случае.
        """
        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    user = Users(telegram_id=telegram_id)
                    session.add(user)
                    session.commit()

                shelf_item = (
                    session.query(UserShelf)
                    .filter_by(user_id=user.id, book_id=book_id)
                    .first()
                )

                if shelf_item:
                    shelf_item.book_status = new_status
                    session.commit()
                    return True
                else:
                    return False

            except IntegrityError:
                session.rollback()
                return False

    def remove_book_from_shelf(
            self,
            telegram_id: int,
            book_id: int
    ) -> bool:
        """Удаляет книгу из полки пользователя.

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги, которую нужно удалить.

        Returns:
            True, если книга успешно удалена, False в противном случае.
        """
        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    user = Users(telegram_id=telegram_id)
                    session.add(user)
                    session.commit()

                shelf_item = (
                    session.query(UserShelf)
                    .filter_by(user_id=user.id, book_id=book_id)
                    .first()
                )

                if shelf_item:
                    session.delete(shelf_item)
                    session.commit()
                    return True
                else:
                    return False

            except Exception:
                session.rollback()
                return False

    def search_book(self, query: str) -> list[BookInfoTypedDict]:
        """Ищет книги по совпадению в имени или авторе

        Args:
            query: Поисковый запрос.

        Returns:
            Список найденных книг.
        """

        with self.__sessionmaker() as session:

            query = f"%{query}%"  # Добавляем wildcards для поиска по частичному совпадению
            books_ = (
                session.query(Books)
                .filter(
                    or_(
                        Books.name.like(query),
                        Books.author.like(query)
                    )
                )
                .all()
            )


            books: list[BookInfoTypedDict] = [
                {
                    "book_id": int(item.id),
                    "litres_id": int(item.litres_id),
                    "picture": str(item.picture),
                    "description": str(item.description),
                    "author": str(item.author),
                    "name": str(item.name)
                }
                for item in books_
            ]

        return books

    def get_books_by_ids(self, book_ids: List[int]) -> list[Type[Books]]:
        """Получает книги из базы данных по списку ID.

        Args:
            book_ids: Список ID книг, которые нужно получить.

        Returns:
            Список объектов `Books` из базы данных, соответствующих указанным ID.
        """
        with self.__sessionmaker() as session:
            books = session.query(Books).filter(Books.id.in_(book_ids)).all()
            return books