from aiogram.types import (KeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, InlineKeyboardButton)


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="\U0001F4DA Прочитанные"), KeyboardButton(text="\U00002B50 Рекомендации")],
    [KeyboardButton(text="\U0001F495 Избранное"), KeyboardButton(text="\U0001F50E Поиск")],
], resize_keyboard=True)


def get_swiper_menu(index: int, length: int, isFavourite: bool = False):
    keyboard = [[]]
    if index > 0:
        keyboard[0].append(InlineKeyboardButton(text="<<",callback_data="prev"))
    keyboard[0].append(InlineKeyboardButton(text=f'({index+1}/{length})', callback_data="a"))

    if index < length - 1:
        keyboard[0].append(InlineKeyboardButton(text=">>",callback_data="next"))
    if isFavourite:
        keyboard.append([InlineKeyboardButton(text='\U00002716 Удалить из избранного', callback_data="toggleFavourite")])
    else:
        keyboard.append([InlineKeyboardButton(text='\U00002795 Добавить в избранное', callback_data="toggleFavourite")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



