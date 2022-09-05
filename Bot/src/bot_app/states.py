from aiogram.dispatcher.filters.state import State, StatesGroup


class GameStates(StatesGroup):
    random_word = State()


class MenuManager(StatesGroup):
    menu = State()


class AddWord(StatesGroup):
    end_word = State()
    ukr_word = State()
    category = State()


