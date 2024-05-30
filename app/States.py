from aiogram.fsm.state import State, StatesGroup


# Состояние для вкладки "Прочитанные"
class Readen(StatesGroup):
    booksArr = State()
    currentIndex = State()