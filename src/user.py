from aiogram import types


class User:
    id = -1
    username = ''
    access = False

    def __init__(self, data: types.Message = None):
        if data is None:
            return
        self.username = data.chat.username
        self.id = data.chat.id

    def json(self) -> dict:
        return {
            'id': int(self.id),
            'username': self.username,
            'access': self.access,
        }

    def set(self, data: dict):
        self.id = int(data.get('id'))
        self.username = data.get('username')
        self.access = data.get('access')
