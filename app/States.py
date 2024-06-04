from aiogram.fsm.state import State, StatesGroup


# Состояние для вкладки "Прочитанные"
class Readen(StatesGroup):
    pass


# Состояние для вкладки "Избранное"
class Favorite(StatesGroup):
    pass


# Состояние для вкладки "Поиск"
class Search(StatesGroup):
    input = State()
