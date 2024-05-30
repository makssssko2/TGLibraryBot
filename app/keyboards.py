from aiogram.types import (KeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, InlineKeyboardButton)


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="\U0001F4DA Прочитанные"),KeyboardButton(text="\U00002B50 Рекомендации")],
    [KeyboardButton(text="\U0001F495 Избранное")],
],resize_keyboard=True)

def get_swiperMenu(index: int,length: int):
    keyboard = [[]]
    if index > 0: keyboard[0].append(InlineKeyboardButton(text="<<",callback_data="prev"))
    keyboard[0].append(InlineKeyboardButton(text=f'({index+1}/{length})', callback_data="a"))
    if index < length - 1: keyboard[0].append(InlineKeyboardButton(text=">>",callback_data="next"))

    keyboard.append([InlineKeyboardButton(text='\U00002705 Добавить в избранное', callback_data="addFavourite")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



