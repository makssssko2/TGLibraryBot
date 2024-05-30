from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import app.States as st
import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('<b>Вжухх !</b>\n\nСкорее добавляй свои книги в "Прочитанные" и я подберу тебе что-нибудь.',reply_markup=kb.main_menu,parse_mode=ParseMode.HTML)


@router.message(F.text == '\U0001F4DA Прочитанные')
async def cmd_books(message: Message, state: FSMContext):
    state.clear()
    await state.set_state(st.Readen)
    await state.update_data(booksArr= [
                                        {
                                            'image': 'https://sun9-44.userapi.com/impf/c631929/v631929682/1d7b9/rFSOkvhanto.jpg?size=604x496&quality=96&sign=037d7a494759a107dd54d1d87886b891&type=album',
                                            'name': 'Как жить с огромным членом ?', 'author': 'Поркшеян В.М',
                                            'description': 'Описание описание описание описание описание описание',
                                            'favourite': False},
                                        {
                                            'image': 'https://aigis.club/uploads/posts/2022-05/1653072677_11-adonius-club-p-oboi-s-obezyanami-krasivie-15.jpg',
                                            'name': 'Почему я преподаю ИИ', 'author': 'Ляхницкая О.В',
                                            'description': 'Описание описание описание описание описание описание',
                                            'favourite': False},
                                        {
                                            'image': 'https://zefirka.net/wp-content/uploads/2020/06/serdityj-kot-kotoryj-oxranyaet-arbuznuyu-fermu-v-tailande-1.jpg',
                                            'name': 'Биография', 'author': 'Иванов И.И',
                                            'description': 'Описание описание описание описание описание описание',
                                            'favourite': False},
                                       {
                                           'image': 'https://sun9-44.userapi.com/impf/c631929/v631929682/1d7b9/rFSOkvhanto.jpg?size=604x496&quality=96&sign=037d7a494759a107dd54d1d87886b891&type=album',
                                           'name': 'Как жить с огромным членом ?', 'author': 'Поркшеян В.М',
                                           'description': 'Описание описание описание описание описание описание',
                                           'favourite': False},
                                       {
                                           'image': 'https://aigis.club/uploads/posts/2022-05/1653072677_11-adonius-club-p-oboi-s-obezyanami-krasivie-15.jpg',
                                           'name': 'Почему я преподаю ИИ', 'author': 'Ляхницкая О.В',
                                           'description': 'Описание описание описание описание описание описание',
                                           'favourite': False},
                                       {
                                           'image': 'https://zefirka.net/wp-content/uploads/2020/06/serdityj-kot-kotoryj-oxranyaet-arbuznuyu-fermu-v-tailande-1.jpg',
                                           'name': 'Биография', 'author': 'Иванов И.И',
                                           'description': 'Описание описание описание описание описание описание',
                                           'favourite': False},
           ])
    await state.update_data(currentIndex=0)

    data = await state.get_data()
    books = data["booksArr"]
    index = data["currentIndex"]
    await message.answer_photo(books[index]['image'],f'<b>{books[index]["author"]} - {books[index]["name"]}</b>\n\n{books[index]["description"]}',
                               reply_markup=kb.get_swiperMenu(index,len(books),books[index]["favourite"]),
                               parse_mode=ParseMode.HTML)

@router.callback_query(F.data == 'next')
async def nextBook(callback: CallbackQuery,state: FSMContext):
    data = await state.get_data()
    await state.update_data(currentIndex=data["currentIndex"] + 1)
    # Костыльно сделано базару нет, но просто когда мы делаем апдейт - data не изменяется и вариант только вводить еще одну переменную index
    # либо заново подгружать обновленные данные и брать индекс оттуда. Если найдешь лучший вариант - исправь
    index = data["currentIndex"] + 1
    books = data["booksArr"]
    await callback.message.edit_media(InputMediaPhoto(media=books[index]['image'],
                                                      caption=f'<b>{books[index]["author"]} - {books[index]["name"]}</b>\n\n{books[index]["description"]}',
                                                      parse_mode=ParseMode.HTML,
                                                      ))
    await callback.message.edit_reply_markup(reply_markup=kb.get_swiperMenu(index,len(books),books[index]["favourite"]))


@router.callback_query(F.data == 'prev')
async def prevBook(callback: CallbackQuery,state: FSMContext):
    data = await state.get_data()
    await state.update_data(currentIndex=data["currentIndex"] - 1)
    # Костыльно сделано базару нет, но просто когда мы делаем апдейт - data не изменяется и вариант только вводить еще одну переменную index
    # либо заново подгружать обновленные данные и брать индекс оттуда. Если найдешь лучший вариант - исправь
    index = data["currentIndex"] - 1
    books = data["booksArr"]
    await callback.message.edit_media(InputMediaPhoto(media=books[index]['image'],
                                                      caption=f'<b>{books[index]["author"]} - {books[index]["name"]}</b>\n\n{books[index]["description"]}',
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