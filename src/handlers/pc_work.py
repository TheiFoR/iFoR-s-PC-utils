import os
from aiogram import Router, Bot, types, F
from aiogram.fsm.context import FSMContext

from src import database
from src.states import States

dp = Router()

bot: Bot = None


@dp.message(States.menu and F.text == database.keyboard_text['menu'][0])
async def pc_off(message: types.Message, state: FSMContext):
    from main import keyboards, debug
    await message.answer(text=database.text.menu.pc_off, reply_markup=keyboards.menu.markup())
    if not debug:
        await os.system("shutdown /s /t 0")


@dp.message(States.menu and F.text == database.keyboard_text['menu'][1])
async def pc_restart(message: types.Message, state: FSMContext):
    from main import keyboards, debug
    await message.answer(text=database.text.menu.pc_restart, reply_markup=keyboards.menu.markup())
    if not debug:
        await os.system("shutdown /r /t 0")
