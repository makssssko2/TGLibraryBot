from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message
import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('<b>Вжухх !</b>\n\nСкорее добавляй свои книги в "Прочитанные" и я подберу тебе что-нибудь.',reply_markup=kb.main_menu,parse_mode=ParseMode.HTML)