import asyncio
import json
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src import config, database
from src.handlers import access, pc_off
from src.states import States
from src.user import User
from src.utils import keyboard

bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

keyboards = keyboard.get(database.keyboard_text, database.keyboard_parameters)


@dp.message(Command('start'))
async def message(message: types.Message, state: FSMContext):
    if database.getAccess(message):
        await message.answer(text=database.text.access(message), reply_markup=keyboards.menu.markup())
        await state.set_state(States.menu)
    else:
        await message.answer(text=database.text.no_access, reply_markup=keyboards.no_access.markup())
        await state.set_state(States.no_access)


async def main():
    logging.basicConfig(level=logging.DEBUG)

    dp.include_router(access.dp)
    dp.include_router(pc_off.dp)

    access.bot = bot
    pc_off.bot = bot

    database._database_path = str(Path(__file__).parent) + "\\users_database.json"

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
