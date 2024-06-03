from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import app.States as st
import app.keyboards as kb
from config import STATIC_DATA
from DB.DB import DB

router = Router()
db = DB()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(st.Readen)
    await state.update_data(booksArr=STATIC_DATA)
    await state.update_data(currentIndex=0)

    await message.answer('<b>Вжухх !</b>\n\nСкорее добавляй свои книги в "Прочитанные" и я подберу тебе что-нибудь.',
                         reply_markup=kb.main_menu,
                         parse_mode=ParseMode.HTML)


@router.message(F.text == '\U0001F4DA Прочитанные')
async def cmd_books(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(st.Readen)
    await state.update_data(booksArr=STATIC_DATA)
    await state.update_data(currentIndex=0)

    data = await state.get_data()
    books = db.get_user_bookshelf(message.chat.id)

    if len(books) == 0:
        await message.answer(
            '<b>Пока что не одна книга не добавленна в "Прочитанные"!</b>\n\nНайти свою любимую книгу можно в меню <b>"Поиск"</b>',
            reply_markup=kb.main_menu,
            parse_mode=ParseMode.HTML)
        return

    index = data["currentIndex"]

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await message.answer_photo(books[index]['picture'],
                               caption,
                               reply_markup=kb.get_swiper_menu(
                                   index,
                                   len(books),
                                   db.is_book_favorite(message.chat.id, books[index]['book_id'])
                               ),
                               parse_mode=ParseMode.HTML)


@router.message(F.text == '\U0001F495 Избранное')
async def cmd_favourite(message: Message, state: FSMContext):
    data = await state.get_data()

    await state.clear()
    await state.set_state(st.Favorite)
    await state.update_data(currentIndex=0)

    data = await state.get_data()
    books = db.get_user_favorites(message.chat.id)

    if(len(books) == 0):
        await message.answer(
            '<b>Пока что не одна книга не добавленна в "Избранное"!</b>\n\nНайти свою любимую книгу можно в меню <b>"Поиск"</b>',
            reply_markup=kb.main_menu,
            parse_mode=ParseMode.HTML)
        return

    index = data["currentIndex"]

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await message.answer_photo(books[index]['picture'],
                               caption,
                               reply_markup=kb.get_swiper_menu(index, len(books), db.is_book_favorite(message.chat.id, books[index]['book_id'])),
                               parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'next')
async def nextBook(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    data["currentIndex"] += 1
    await state.update_data(currentIndex=data["currentIndex"])

    index = data["currentIndex"]

    if await state.get_state() == st.Readen:
        books = db.get_user_bookshelf(callback.message.chat.id)
    else:
        books = db.get_user_favorites(callback.message.chat.id)
    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await callback.message.edit_media(
        InputMediaPhoto(
            media=books[index]['picture'],
            caption=caption,
            parse_mode=ParseMode.HTML
        ))
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_swiper_menu(
            index,
            len(books),
            db.is_book_favorite(callback.message.chat.id, books[index]['book_id'])
        )
    )


@router.callback_query(F.data == 'prev')
async def prevBook(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    data["currentIndex"] -= 1
    await state.update_data(currentIndex=data["currentIndex"])

    index = data["currentIndex"]
    if await state.get_state() == st.Readen:
        books = db.get_user_bookshelf(callback.message.chat.id)
    else:
        books = db.get_user_favorites(callback.message.chat.id)

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await callback.message.edit_media(
        InputMediaPhoto(
            media=books[index]['picture'],
            caption=caption,
            parse_mode=ParseMode.HTML
        ))
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_swiper_menu(
            index,
            len(books),
            db.is_book_favorite(callback.message.chat.id, books[index]['book_id'])
        )
    )


@router.callback_query(F.data == 'toggleFavourite')
async def toggleFavourite(callback: CallbackQuery,state: FSMContext):
    data = await state.get_data()
    index = data["currentIndex"]

    if await state.get_state() == st.Readen:
        books = db.get_user_bookshelf(callback.message.chat.id)
    else:
        books = db.get_user_favorites(callback.message.chat.id)

    is_favorite = db.is_book_favorite(callback.message.chat.id, books[index]['book_id'])
    if is_favorite:
        db.remove_book_from_favorites(callback.message.chat.id, books[index]['book_id'])
        if await state.get_state() == st.Favorite:
            if index > 0:
                data['currentIndex'] -= 1
            books = db.get_user_favorites(callback.message.chat.id)
            await state.update_data(currentIndex=data["currentIndex"])
            index = data["currentIndex"]
        if len(books) == 0:
            await callback.message.answer(
                '<b>Пока что не одна книга не добавленна в "Избранное"!</b>\n\nНайти свою любимую книгу можно в меню <b>"Поиск"</b>',
                reply_markup=kb.main_menu,
                parse_mode=ParseMode.HTML
            )
            await callback.message.delete()
            return
    else:
        db.add_book_to_favorites(callback.message.chat.id, books[index]['book_id'])

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await callback.message.edit_media(
        InputMediaPhoto(
            media=books[index]['picture'],
            caption=caption,
            parse_mode=ParseMode.HTML
        ))
    await callback.message.edit_reply_markup(
        reply_markup=kb.get_swiper_menu(
            index,
            len(books),
            db.is_book_favorite(callback.message.chat.id, books[index]['book_id'])
        )
    )
