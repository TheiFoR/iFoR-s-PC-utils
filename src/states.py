from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    settings = State()
    auto_off_menu = State()
    menu = State()
    no_access = State()
    send_access = State()
