from aiogram.fsm.state import State, StatesGroup


# Состояние для вкладки "Прочитанные"
class Readen(StatesGroup):
    currentIndex = State()


# Состояние для вкладки "Избранное"
class Favorite(StatesGroup):
    currentIndex = State()

# Состояние для вкладки "Поиск"
class Search(StatesGroup):
    currentIndex = State()
    input = State()

