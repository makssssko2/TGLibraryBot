from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Books(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    litres_id: Mapped[int]
    url: Mapped[str]
    picture: Mapped[str]
    author: Mapped[str]
    name: Mapped[str]
    publisher: Mapped[str] = mapped_column(nullable=True)
    series: Mapped[str]
    year: Mapped[str] = mapped_column(nullable=True)
    ISBN: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str]
    age: Mapped[int]
    lang: Mapped[str]
    litres_isbn: Mapped[str] = mapped_column(nullable=True)
    genres: Mapped[str]


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]


class UserShelf(Base):
    __tablename__ = 'user_shelf'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    book = relationship("Books")


class UserFavorite(Base):
    __tablename__ = 'user_favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    book = relationship("Books")
