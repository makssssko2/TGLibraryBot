from typing import List, Type
from sqlalchemy import create_engine, text, func, Table, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker
from .models import Base, Books, Users, UserShelf, UserFavorite, TGCard
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from .TypedDict.BooksTypedDict import BookInfoTypedDict


class DB:

    def __init__(self):
        self.__engine = create_engine('sqlite:///AI.db')
        Base.metadata.create_all(self.__engine)
        self.__sessionmaker = sessionmaker(bind=self.__engine)
        self._search_content = None

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
            book_id: int
    ) -> bool:
        """Добавляет книгу в полку пользователя.
           Если пользователя нет в базе данных, то он создаётся.
           Если книга уже есть у пользователя, то возвращается False.

        Args:
            telegram_id: Telegram ID пользователя,
            book_id: ID книги.

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

                existing_item = session.query(UserShelf).filter_by(
                    user_id=user.id,
                    book_id=book_id
                ).first()

                if existing_item:
                    return False

                new_shelf_item = UserShelf(
                    user_id=user.id,
                    book_id=book_id
                )
                session.add(new_shelf_item)
                session.commit()
                return True

            except IntegrityError:
                session.rollback()
                return False

    def get_user_bookshelf(self, telegram_id: int) -> list[BookInfoTypedDict]:
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

            books: list[BookInfoTypedDict] = [
                {
                    "book_id": item.book.id,
                    "litres_id": item.book.litres_id,
                    "picture": item.book.picture,
                    "description": item.book.description,
                    "author": item.book.author,
                    "name": item.book.name,
                    "publisher": item.book.publisher,
                    "year": item.book.year
                }
                for item in bookshelf_items
            ]

            return books

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
                    "name": str(item.name),
                    "publisher": str(item.publisher),
                    "year": str(item.year)
                }
                for item in books_
            ]

        return books

    def get_books_by_ids(self, book_ids: List[int]) -> list[BookInfoTypedDict]:
        """Получает книги из базы данных по списку ID.

        Args:
            book_ids: Список ID книг, которые нужно получить.

        Returns:
            Список объектов `Books` из базы данных, соответствующих указанным ID.
        """
        with self.__sessionmaker() as session:
            books_ = session.query(Books).filter(Books.id.in_(book_ids)).all()
            books: list[BookInfoTypedDict] = [
                {
                    "book_id": int(item.id),
                    "litres_id": int(item.litres_id),
                    "picture": str(item.picture),
                    "description": str(item.description),
                    "author": str(item.author),
                    "name": str(item.name),
                    "publisher": str(item.publisher),
                    "year": str(item.year)
                }
                for item in books_
            ]
            return books

    def add_book_to_favorites(self, telegram_id: int, book_id: int) -> bool:
        """Добавляет книгу в избранное пользователя.
           Если пользователя нет в базе данных, то он создаётся.
           Если книга уже есть в избранном, то возвращается False.

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги.

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

                existing_item = session.query(UserFavorite).filter_by(
                    user_id=user.id, book_id=book_id
                ).first()

                if existing_item:
                    return False

                new_favorite_item = UserFavorite(
                    user_id=user.id, book_id=book_id
                )
                session.add(new_favorite_item)
                session.commit()
                return True

            except IntegrityError:
                session.rollback()
                return False

    def remove_book_from_favorites(self, telegram_id: int, book_id: int) -> bool:
        """Удаляет книгу из избранного пользователя.
           Если пользователя нет в базе данных, то он не создаётся.

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги.

        Returns:
            True, если книга успешно удалена, False в противном случае.
        """

        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    return False

                favorite_item = (
                    session.query(UserFavorite)
                    .filter_by(user_id=user.id, book_id=book_id)
                    .first()
                )

                if favorite_item:
                    session.delete(favorite_item)
                    session.commit()
                    return True

                return False

            except Exception:
                session.rollback()
                return False

    def get_user_favorites(self, telegram_id: int) -> List[BookInfoTypedDict]:
        """Возвращает список избранных книг пользователя по его telegram_id.

        Args:
            telegram_id: Telegram ID пользователя.

        Returns:
            Список BookInfoTypedDict, представляющих избранные книги пользователя.
        """

        with self.__sessionmaker() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()

            if not user:
                user = Users(telegram_id=telegram_id)
                session.add(user)
                session.commit()

            favorite_books = (
                session.query(UserFavorite)
                .options(joinedload(UserFavorite.book))
                .filter(UserFavorite.user_id == user.id)
                .all()
            )

            books: List[BookInfoTypedDict] = [
                {
                    "book_id": item.book.id,
                    "litres_id": item.book.litres_id,
                    "picture": item.book.picture,
                    "description": item.book.description,
                    "author": item.book.author,
                    "name": item.book.name,
                    "publisher": item.book.publisher,
                    "year": item.book.year
                }
                for item in favorite_books
            ]

            return books

    def is_book_readen(self, telegram_id: int, book_id: int) -> bool:
        """Проверяет прочитанная книга или нет

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги.

        Returns:
            True, если книга в избранном, False в противном случае.
        """

        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    return False

                favorite_item = (
                    session.query(UserShelf)
                    .filter_by(user_id=user.id, book_id=book_id)
                    .first()
                )

                if favorite_item:
                    return True

                return False

            except Exception:
                session.rollback()
                return False

    def is_book_favorite(self, telegram_id: int, book_id: int) -> bool:
        """Проверяет в избранном книга или нет

            Args:
                telegram_id: Telegram ID пользователя.
                book_id: ID книги.

            Returns:
                True, если книга в избранном, False в противном случае.
            """

        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    return False

                favorite_item = (
                    session.query(UserFavorite)
                    .filter_by(user_id=user.id, book_id=book_id)
                    .first()
                )

                if favorite_item:
                    return True

                return False

            except Exception:
                session.rollback()
                return False

    def toggle_favorite(self, telegram_id: int, book_id: int) -> bool:
        """Добавляет или удаляет книгу из избранного пользователя в зависимости от её текущего статуса.

        Args:
            telegram_id: Telegram ID пользователя.
            book_id: ID книги.

        Returns:
            True, если операция выполнена успешно, False в противном случае.
        """

        with self.__sessionmaker() as session:
            try:
                user = session.query(Users).filter_by(telegram_id=telegram_id).first()

                if not user:
                    user = Users(telegram_id=telegram_id)
                    session.add(user)
                    session.commit()

                favorite_item = session.query(UserFavorite).filter_by(
                    user_id=user.id, book_id=book_id
                ).first()

                if favorite_item:
                    session.delete(favorite_item)
                    session.commit()
                    return True
                else:
                    new_favorite_item = UserFavorite(
                        user_id=user.id, book_id=book_id
                    )
                    session.add(new_favorite_item)
                    session.commit()
                    return True

            except IntegrityError:
                session.rollback()
                return False

    def add_tg_card(
            self,
            telegram_id: int,
            message_id: int,
            current_index: int,
            books_id: List[int],
    ) -> None:
        """Добавляет запись в таблицу TGCard.

        Args:
            telegram_id: Telegram ID пользователя.
            message_id: ID сообщения в Telegram.
            current_index: Текущий индекс в списке книг.
            books_id: Список ID книг.
        """

        with self.__sessionmaker() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()

            if not user:
                user = Users(telegram_id=telegram_id)
                session.add(user)
                session.commit()

            books_id_str = ",".join(map(str, books_id))

            new_card = TGCard(
                user_id=user.id,
                message_id=message_id,
                current_index=current_index,
                books_id=books_id_str,
            )
            session.add(new_card)
            session.commit()

    def update_tg_card(
            self,
            telegram_id: int,
            message_id: int,
            current_index: int,
            books_id: List[int],
    ) -> bool:
        """Обновляет запись в таблице TGCard.

        Args:
            telegram_id: Telegram ID пользователя.
            message_id: ID сообщения в Telegram.
            current_index: Новый текущий индекс в списке книг.
            books_id: Новый список ID книг.

        Returns:
            True, если обновление прошло успешно, False в противном случае.
        """

        with self.__sessionmaker() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()

            if not user:
                return False

            card = (
                session.query(TGCard)
                .filter_by(user_id=user.id, message_id=message_id)
                .first()
            )

            if not card:
                return False

            card.current_index = current_index
            card.books_id = ",".join(map(str, books_id))

            session.commit()
            return True

    def get_tg_card(
            self, telegram_id: int, message_id: int
    ) -> tuple[int, List[BookInfoTypedDict]] | None:
        """Получает TGCard и информацию о книгах.

        Args:
            telegram_id: Telegram ID пользователя.
            message_id: ID сообщения в Telegram.

        Returns:
            Кортеж из current_index и списка информации о книгах в формате BookInfoTypedDict,
            или None, если карточка не найдена.
        """

        with self.__sessionmaker() as session:
            user = session.query(Users).filter_by(telegram_id=telegram_id).first()


            card = (
                session.query(TGCard)
                .filter_by(user_id=user.id, message_id=message_id)
                .first()
            )

            if not card:
                return None

            book_ids = list(map(int, card.books_id.split(",")))
            books = session.query(Books).filter(Books.id.in_(book_ids)).all()

            book_info_list: List[BookInfoTypedDict] = [
                {
                    "book_id": int(book.id),
                    "litres_id": int(book.litres_id),
                    "picture": str(book.picture),
                    "author": str(book.author),
                    "name": str(book.name),
                    "publisher": str(book.publisher),
                    "description": str(book.description),
                    "year": str(book.year),
                }
                for book in books
            ]

            return card.current_index, book_info_list
