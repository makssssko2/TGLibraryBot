from aiogram.fsm.state import State, StatesGroup


# Состояние для вкладки "Прочитанные"
class Readen(StatesGroup):
    books = State()
    currentIndex = State()


# Состояние для вкладки "Избранное"
class Favorite(StatesGroup):
    books = State()
    currentIndex = State()

