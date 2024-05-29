from aiogram.types import (KeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, InlineKeyboardButton)


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="\U0001F4DA Прочитанные"),KeyboardButton(text="\U00002B50 Рекомендации")],
    [KeyboardButton(text="\U0001F495 Избранное")],
],resize_keyboard=True)