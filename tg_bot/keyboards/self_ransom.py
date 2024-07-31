from aiogram import types


def self_ransom():
    btn_1 = types.InlineKeyboardButton(text="Видео-инструкция", url="https://t.me/c/1581391502/140")
    btn_2 = types.InlineKeyboardButton(text="Условия самовыкупа", url="https://t.me/c/1581391502/154")
    btn_3 = types.InlineKeyboardButton(text="Отправить бланк заказов", url="https://t.me/Vanish0_p")
    btn_4 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="return start menu after self ransom")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2], [btn_3], [btn_4]])
    return keyboard

