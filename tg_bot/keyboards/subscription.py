from aiogram import types


def create_subscription_keyboard():
    btn_1 = types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/vanish_cn")
    cb_btn = types.InlineKeyboardButton(text="Проверить подписку", callback_data="subscription verification")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [cb_btn]])
    return keyboard


def start_menu():
    btn_1 = types.InlineKeyboardButton(text="Поиск прямых производств", callback_data="direct production")
    btn_2 = types.InlineKeyboardButton(text="Самовыкуп", callback_data="self ransom")
    btn_3 = types.InlineKeyboardButton(text="Обменять рубли на юани", callback_data="exchange")
    btn_4 = types.InlineKeyboardButton(text="Доставка - Условия", callback_data="delivery condition")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2], [btn_3], [btn_4]])
    return keyboard
