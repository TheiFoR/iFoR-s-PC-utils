import re
from aiogram import Router, Bot, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from main import keyboards
from src import database
from src.states import States

dp = Router()

bot: Bot = None


@dp.message(States.no_access)
async def send_access(message: types.Message, state: FSMContext):
    await bot.send_message(database.father_id, database.text.access_request(message),
                           reply_markup=keyboards.access_request.markup())
    await message.answer(text=database.text.send_access, reply_markup=keyboards.no_access.markup())
    await state.set_state(States.send_access)


@dp.message(States.send_access)
async def access_sent(message: types.Message, state: FSMContext):
    await message.answer(text=database.text.access_sent, reply_markup=keyboards.no_access.markup())
    await state.set_state(States.send_access)


@dp.callback_query(F.data.startswith('access_success'))
async def access_success(call: CallbackQuery, state: FSMContext):
    id = int(re.search("(?!Id: )\d+", call.message.text).group())

    database.setAccess(id, True)

    await bot.send_message(id, database.text.access_success, reply_markup=keyboards.user_access_success.markup())

    await call.message.edit_text(call.message.text + database.text.callback_access_success)
    await call.answer()


@dp.callback_query(F.data.startswith('access_failed'))
async def access_failed(call: CallbackQuery, state: FSMContext):
    id = int(re.search("(?!Id: )\d+", call.message.text).group())

    await bot.send_message(id, database.text.access_failed, reply_markup=keyboards.user_access_failed.markup())

    await call.message.edit_text(call.message.text + database.text.callback_access_failed)
    await call.answer()


@dp.callback_query(F.data.startswith('user_access_success'))
async def access_failed(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(database.text.pc_menu, reply_markup=keyboards.menu.markup())
    await call.answer()
    await state.set_state(States.menu)


@dp.callback_query(F.data.startswith('user_access_failed'))
async def access_failed(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(database.text.no_access, reply_markup=keyboards.no_access.markup())
    await call.answer()
    await state.set_state(States.no_access)
