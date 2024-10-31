import re
from aiogram import Router, Bot, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src import database
from src.states import States

dp = Router()

bot: Bot = None


# *** ***

@dp.message(States.menu and F.text == database.keyboard_text['menu'][2])
async def send_access(message: types.Message, state: FSMContext):
    from main import keyboards
    await message.answer(text=database.text.settings.label, reply_markup=keyboards.settings.markup())
    await state.set_state(States.settings)


# *** ***

@dp.message(States.settings and F.text == database.keyboard_text['settings'][0])
async def access_sent(message: types.Message, state: FSMContext):
    from main import keyboards
    await message.answer(text=database.text.access_sent, reply_markup=keyboards.auto_off.markup())
    await state.set_state(States.auto_off_menu)


@dp.message(States.settings and F.text == database.keyboard_text['settings'][-1])
async def access_sent(message: types.Message, state: FSMContext):
    from main import keyboards
    await message.answer(text=database.text.menu.label, reply_markup=keyboards.menu.markup())
    await state.set_state(States.menu)


# *** ***

@dp.message(States.auto_off_menu and F.text == database.keyboard_text['auto_off'][-1])
async def access_sent(message: types.Message, state: FSMContext):
    from main import keyboards
    await message.answer(text=database.text.settings.auto_off.label, reply_markup=keyboards.settings.markup())
    await state.set_state(States.settings)