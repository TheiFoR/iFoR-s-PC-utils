import json
import os
from pathlib import Path

from aiogram import types

from src.user import User

father_id = 747120601


_database_path = ''


class text:
    no_access = "<b>🚫 У вас нет доступа.</b> 🔒\n\n"\
                "Чтобы получить доступ, отправьте запрос администратору 📩"
    send_access = "Запрос отправлен 📨"
    access_sent = "Запрос уже отправлен 📨, ожидайте ответа ⏳."

    access_success = "<b>✅ Доступ получен!</b>\n" \
                     "\n" \
                     "Приятного пользования! 💻"
    access_failed = "<b>❌Отказ в доступе❌</b>\n" \
                    "\n" \
                    "Попробуйте позднее ⏳"

    callback_access_success = "\n\n<b>Решение: ✅</b>"
    callback_access_failed = "\n\n<b>Решение: ❌</b>"

    pc_menu = "<b>Главная: 📑</b>"

    pc_off = "<b>Выключаем ⏻</b>\n" \
             "\n" \
             "Бот будет выключен вместе с ПК 🖥️🔌"

    pc_restart = "<b>🔄 Перезагружаем</b>\n" \
             "\n" \
             "Бот будет перезагружаем вместе с ПК 🖥️🔌"

    @staticmethod
    def access_request(message: types.Message) -> str:
        user = User(message)
        return f"<b>🖥️ Запрос на доступ к ПК от:</b>\n" \
               f"\n" \
               f"🆔 Id: {user.id}\n" \
               f"👤 Username: @{user.username}\n"

    @staticmethod
    def access(message: types.Message) -> str:
        return f"👋 С возвращением, <b>{message.chat.username}</b>!"


keyboard_text = {
    'no_access': ['🔓Запросить доступ'],
    'menu': ['❌ Выключить ❌', '🔄 Перезагрузка 🔄'],
    'user_access_success': ['Начать 🚀'],
    'user_access_failed': ['Назад ⬅️'],
    'access_request': ['✅', '❌']
}
keyboard_parameters = {
    'access_request': {
        'inline_callbacks': ['access_success', 'access_failed']
    },
    'user_access_success': {
        'inline_callbacks': ['user_access_success']
    },
    'user_access_failed': {
        'inline_callbacks': ['user_access_failed']
    }
}


def getAccess(message: types.Message) -> bool:
    user = User(message)
    if not os.path.exists(_database_path):
        setDefault(message)
        return False
    try:
        with open(_database_path, 'r+') as file:
            if os.stat(_database_path).st_size == 0:
                setDefault(message)
                return False
            users: dict = json.load(file)
        if users.get(str(user.id)) is not None:
            user.set(users.get(str(user.id)))
            return user.access
        else:
            with open(_database_path, 'w') as file:
                data = users
                data[user.id] = user.json()
                json.dump(data, file, indent=4)
            return False
    except (json.JSONDecodeError, IOError):
        setDefault(message)
        return False


def setDefault(message: types.Message):
    user = User(message)
    with open(_database_path, 'w') as file:
        json.dump({user.id: user.json()}, file, indent=4)


def setAccess(id: int, access: bool):
    with open(_database_path, 'r') as file:
        users: dict = json.load(file)

    user = User()
    user.set(users.get(str(id)))
    user.access = access
    users[str(id)] = user.json()

    with open(_database_path, 'w') as file:
        json.dump(users, file, indent=4)