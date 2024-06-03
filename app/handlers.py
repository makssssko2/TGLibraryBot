from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import app.States as st
import app.keyboards as kb
from config import STATIC_DATA

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    state.clear()
    state.set_state(st.Readen)
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

    if (len(data["booksArr"]) == 0):
        await message.answer(
            '<b>Пока что не одна книга не добавленна в "Прочитанные"!</b>\n\nНайти свою любимую книгу можно в меню <b>"Поиск"</b>',
            reply_markup=kb.main_menu,
            parse_mode=ParseMode.HTML)
        return

    books = data["booksArr"]
    index = data["currentIndex"]

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await message.answer_photo(books[index]['image'],
                               caption,
                               reply_markup=kb.get_swiperMenu(index,len(books),books[index]["favourite"]),
                               parse_mode=ParseMode.HTML)

@router.message(F.text == '\U0001F495 Избранное')
async def cmd_favourite(message: Message, state: FSMContext):
    data = await state.get_data()

    await state.clear()
    await state.set_state(st.Favorite)
    await state.update_data(booksArr=list(item for item in data["booksArr"] if item["favourite"]))
    await state.update_data(currentIndex=0)

    data = await state.get_data()

    if(len(data["booksArr"]) == 0):
        await message.answer(
            '<b>Пока что не одна книга не добавленна в "Избранное"!</b>\n\nНайти свою любимую книгу можно в меню <b>"Поиск"</b>',
            reply_markup=kb.main_menu,
            parse_mode=ParseMode.HTML)
        return

    books = data["booksArr"]
    index = data["currentIndex"]

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await message.answer_photo(books[index]['image'],
                               caption,
                               reply_markup=kb.get_swiperMenu(index, len(books), books[index]["favourite"]),
                               parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'next')
async def nextBook(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    data["currentIndex"] += 1
    await state.update_data(currentIndex=data["currentIndex"])

    index = data["currentIndex"]
    books = data["booksArr"]

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await callback.message.edit_media(InputMediaPhoto(media=books[index]['image'],
                                                      caption=caption,
                                                      parse_mode=ParseMode.HTML,
                                                      ))
    await callback.message.edit_reply_markup(reply_markup=kb.get_swiperMenu(index,len(books),books[index]["favourite"]))


@router.callback_query(F.data == 'prev')
async def prevBook(callback: CallbackQuery,state: FSMContext):
    data = await state.get_data()

    data["currentIndex"] -= 1
    await state.update_data(currentIndex=data["currentIndex"])

    index = data["currentIndex"]
    books = data["booksArr"]

    caption = f'<b>{books[index]["name"]}\n' \
              f'Автор: {books[index]["author"]}\n\n' \
              f'Издание: {books[index]["publisher"]}\n' \
              f'Год: {books[index]["year"]}</b>' \
              f'\n\n{books[index]["description"]}'

    await callback.message.edit_media(InputMediaPhoto(media=books[index]['image'],
                                                      caption=caption,
                                                      parse_mode=ParseMode.HTML,
                                                      ))
    await callback.message.edit_reply_markup(reply_markup=kb.get_swiperMenu(index, len(books),books[index]["favourite"]))


@router.callback_query(F.data == 'toggleFavourite')
async def toggleFavourite(callback: CallbackQuery,state: FSMContext):
    data = await state.get_data()
    index = data["currentIndex"]
    books = data["booksArr"]
    favourite = books[index]["favourite"]

    books[index]["favourite"] = not favourite

    await state.update_data(booksArr=books)
    await callback.message.edit_reply_markup(reply_markup=kb.get_swiperMenu(index, len(books), not favourite))