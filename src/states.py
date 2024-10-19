from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    menu = State()
    no_access = State()
    send_access = State()
