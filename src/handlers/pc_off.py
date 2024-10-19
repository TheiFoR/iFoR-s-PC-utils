import os
from aiogram import Router, Bot, types, F
from aiogram.fsm.context import FSMContext

from src import database
from src.states import States

dp = Router()

bot: Bot = None


@dp.message(States.menu and F.text == database.keyboard_text['menu'][0])
async def pc_off(message: types.Message, state: FSMContext):
    from main import keyboards
    await message.answer(text=database.text.pc_off, reply_markup=keyboards.menu.markup())
    os.system("shutdown /s /t 0")


@dp.message(States.menu and F.text == database.keyboard_text['menu'][1])
async def pc_restart(message: types.Message, state: FSMContext):
    from main import keyboards
    await message.answer(text=database.text.pc_restart, reply_markup=keyboards.menu.markup())
    await os.system("shutdown /r /t 0")
