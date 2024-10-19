from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class Keyboard:
    def __init__(self, d: dict):
        self.d = d

    def markup(self):
        return self.d

    def __getattr__(self, item: str) -> 'Keyboard':
        return self.__class__(self.d.get(item))

    def __repr__(self):
        return repr(self.d)


def get(keyboards_text, keyboard_settings) -> Keyboard:
    keyboard_objects = {}

    def get_keyboard_object(array_text, width, inline_callbacks, request_contact):
        if inline_callbacks is None:
            keyboard_builder = ReplyKeyboardBuilder()
        else:
            keyboard_builder = InlineKeyboardBuilder()

        if inline_callbacks is None:
            for button_text in array_text:
                keyboard_builder.button(text=button_text, request_contact=request_contact)
        else:
            for i in range(len(array_text)):
                if request_contact is None:
                    keyboard_builder.button(text=array_text[i], callback_data=inline_callbacks[i], request_contact=False)
                else:
                    keyboard_builder.button(text=array_text[i], callback_data=inline_callbacks[i], request_contact=request_contact[i])

        if width is None:
            keyboard_builder.adjust(3)
        elif isinstance(width, int):
            keyboard_builder.adjust(width)
        elif isinstance(width, list):
            keyboard_builder.adjust(*width)

        return keyboard_builder.as_markup(resize_keyboard=True)

    stack = [((), keyboards_text)]

    result_list = []

    while stack:
        path, current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                stack.append((path + (key,), value))
        elif isinstance(current, list):
            for i, value in enumerate(current):
                stack.append((path + (current[i],), value))

            temp_list = list(map(str, path))

            temp_list.append(current)
            result_list.append(temp_list)

    for keyboard_path_array in result_list:
        keyboard_path_array_len = len(keyboard_path_array)
        root_item = keyboard_objects
        for i in range(keyboard_path_array_len):
            if i == keyboard_path_array_len - 2:
                current_settings = keyboard_settings

                for setting_path in keyboard_path_array[:-1]:
                    if current_settings.get(setting_path) is None:
                        current_settings = None
                        break
                    current_settings = current_settings[setting_path]

                current_width_settings = None if current_settings is None else current_settings.get('width')
                current_inline_callback_settings = None if current_settings is None else current_settings.get('inline_callbacks')
                current_request_contact = False if current_settings is None else current_settings.get('request_contact')

                keyboards = get_keyboard_object(list(keyboard_path_array[i + 1]), current_width_settings,
                                                current_inline_callback_settings, current_request_contact)

                root_item[keyboard_path_array[i]] = keyboards
            elif i < keyboard_path_array_len - 2:
                if root_item.get(keyboard_path_array[i]) is None:
                    root_item[keyboard_path_array[i]] = dict()
                root_item = root_item[keyboard_path_array[i]]

    keyboard_objects = Keyboard(keyboard_objects)
    return keyboard_objects
