import datetime
import json
import os
from pathlib import Path

from aiogram import types

from src import settings
from src.user import User

father_id = 747120601


_user_database_path = ''
_database_path = ''


keyboard_text = {
    'no_access': ['🔓Запросить доступ'],
    'menu': ['❌ Выключить', '🔄 Перезагрузка', '⚙️ Настройки'],
    'user_access_success': [' 🚀 Начать'],
    'user_access_failed': ['⬅️ Назад'],
    'access_request': ['✅', '❌'],
    'settings': ['⏰ Автовыключение', '⬅️ Назад'],
    'auto_off': ['🕑 Время', '⏱️Ожидание', '⬅️ Назад'],
    'wait_for_time': ['⏳ 1 мин', '⏳ 3 мин', '⏳ 5 мин', '⏳ 7 мин', '⏳ 10 мин', '⏳ 15 мин'],
    'auto_off_time': ['🕙 10:00 PM', '🕚 11:00 PM', '🕛 12:00 AM', '🕐 1:00 AM']
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
    },
    'menu': {
        'width': [2, 1]
    },
    'auto_off':{
        'width': [2, 1]
    },
    'wait_for_time': {
        'width': [2, 2, 2],
        'inline_callbacks': ['wait_for_time_set', 'wait_for_time_set', 'wait_for_time_set', 'wait_for_time_set', 'wait_for_time_set', 'wait_for_time_set']
    },
    'auto_off_time': {
        'width': [2, 2],
        'inline_callbacks': ['auto_off_time_set', 'auto_off_time_set', 'auto_off_time_set', 'auto_off_time_set']
    },
}

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

    class menu:
        label = "<b>📑 Главная:</b>"

        pc_off = "🌄 <b>Выключаем</b>\n" \
                 "\n" \
                 "Бот будет выключен вместе с ПК 🖥️🔌"

        pc_restart = "<b>🔄 Перезагружаем</b>\n" \
                     "\n" \
                     "Бот будет перезагружаем вместе с ПК 🖥️🔌"

    class settings:
        label = "<b>⚙️Настройки: </b>"

        class auto_off:
            global keyboard_text
            label = "<b>⚙️Настройки автовыключения: </b>\n" \
                    "\n" \
                    f"<b>{keyboard_text['auto_off'][0]}</b> - {settings.auto_off_start_time}" \
                    f"<b>{keyboard_text['auto_off'][0]}</b> - Время, после которого будет включатся автовыключение. Режим с автовыключением отключается в 06:00 AM."



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


def saveSettings():
    with open(_database_path, 'w') as file:
        json.dump({
            'auto_off_start_time': settings.auto_off_start_time,
            'auto_off_wait_for_time': settings.auto_off_wait_for_time,
            'auto_off_polling_time': settings.auto_off_polling_time,
        }, file, indent=4)


def loadSettings():
    if not os.path.exists(_database_path):
        with open(_database_path, 'w') as file:
            json.dump({
                'auto_off_start_time': str(settings.auto_off_start_time),
                'auto_off_wait_for_time': str(settings.auto_off_wait_for_time),
                'auto_off_polling_time': str(settings.auto_off_polling_time),
            }, file, indent=4)
    with open(_database_path, 'r+') as file:
        try:
            data: dict = json.load(file)
        except json.JSONDecodeError:
            data = {}
        settings.auto_off_start_time = datetime.time.strftime(data.get('auto_off_start_time', settings.auto_off_start_time), "%H:%M:%S %p")
        settings.auto_off_wait_for_time = datetime.time.strftime(data.get('auto_off_wait_for_time', settings.auto_off_wait_for_time), "%H:%M:%S")
        settings.auto_off_polling_time = datetime.time.strftime(data.get('auto_off_polling_time', settings.auto_off_polling_time), "%H:%M:%S")


def getAccess(message: types.Message) -> bool:
    user = User(message)
    if not os.path.exists(_user_database_path):
        setDefault(message)
        return False
    try:
        with open(_user_database_path, 'r+') as file:
            if os.stat(_user_database_path).st_size == 0:
                setDefault(message)
                return False
            users: dict = json.load(file)
        if users.get(str(user.id)) is not None:
            user.set(users.get(str(user.id)))
            return user.access
        else:
            with open(_user_database_path, 'w') as file:
                data = users
                data[user.id] = user.json()
                json.dump(data, file, indent=4)
            return False
    except (json.JSONDecodeError, IOError):
        setDefault(message)
        return False


def setDefault(message: types.Message):
    user = User(message)
    with open(_user_database_path, 'w') as file:
        json.dump({user.id: user.json()}, file, indent=4)


def setAccess(id: int, access: bool):
    with open(_user_database_path, 'r') as file:
        users: dict = json.load(file)

    user = User()
    user.set(users.get(str(id)))
    user.access = access
    users[str(id)] = user.json()

    with open(_user_database_path, 'w') as file:
        json.dump(users, file, indent=4)