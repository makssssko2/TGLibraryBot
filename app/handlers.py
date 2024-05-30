from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('<b>Вжухх !</b>\n\nСкорее добавляй свои книги в "Прочитанные" и я подберу тебе что-нибудь.',reply_markup=kb.main_menu,parse_mode=ParseMode.HTML)

Objects = [{'image': 'https://sun9-44.userapi.com/impf/c631929/v631929682/1d7b9/rFSOkvhanto.jpg?size=604x496&quality=96&sign=037d7a494759a107dd54d1d87886b891&type=album','name':'Как жить с огромным членом ?','author':'Поркшеян В.М','description':'Описание описание описание описание описание описание'},
           {'image': 'https://aigis.club/uploads/posts/2022-05/1653072677_11-adonius-club-p-oboi-s-obezyanami-krasivie-15.jpg','name':'Почему я преподаю ИИ','author':'Ляхницкая О.В','description':'Описание описание описание описание описание описание'},
           {'image': 'https://zefirka.net/wp-content/uploads/2020/06/serdityj-kot-kotoryj-oxranyaet-arbuznuyu-fermu-v-tailande-1.jpg','name':'Биография','author':'Иванов И.И','description':'Описание описание описание описание описание описание'}
           ]
# Здесь index сделал чисто для теста и обьекты тоже, потом когда богдан сделает свою часть уберем
index = 1
@router.message(F.text == '\U0001F4DA Прочитанные')
async def cmd_books(message: Message):
    await message.answer_photo(Objects[index]['image'],f'<b>{Objects[index]["author"]} - {Objects[index]["name"]}</b>\n\n{Objects[index]["description"]}',
                               reply_markup=kb.get_swiperMenu(index,len(Objects)),
                               parse_mode=ParseMode.HTML)

@router.callback_query(F.data == 'next')
async def nextBook(callback: CallbackQuery):
    await callback.message.edit_media(InputMediaPhoto(media=Objects[index+1]['image'],
                                                      caption=f'<b>{Objects[index+1]["author"]} - {Objects[index+1]["name"]}</b>\n\n{Objects[index+1]["description"]}',
                                                      parse_mode=ParseMode.HTML,
                                                      ))
    await callback.message.edit_reply_markup(reply_markup=kb.get_swiperMenu(index+1,len(Objects)))


@router.callback_query(F.data == 'prev')
async def prevBook(callback: CallbackQuery):
    await callback.message.edit_media(InputMediaPhoto(media=Objects[index-1]['image'],
                                                      caption=f'<b>{Objects[index-1]["author"]} - {Objects[index-1]["name"]}</b>\n\n{Objects[index-1]["description"]}',
                                                      parse_mode=ParseMode.HTML,
                                                      ))
    await callback.message.edit_reply_markup(reply_markup=kb.get_swiperMenu(index-1,len(Objects)))

