from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    menu = State()