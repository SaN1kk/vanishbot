from aiogram import types


def delivery_cnd():
    btn_1 = types.InlineKeyboardButton(text="Доставка", callback_data="delivery")
    btn_2 = types.InlineKeyboardButton(text="Стоимость", callback_data="price_delivery")
    btn_3 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="return start menu after delivery_cnd")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2], [btn_3]])
    return keyboard


def goods_delivery():
    btn_1 = types.InlineKeyboardButton(text="Видео-инструкция", url="https://youtu.be/DiH-JkgO6HA")
    btn_2 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="return delivery_cnd after delivery")
    btn_3 = types.InlineKeyboardButton(text="Вернуться в начало", callback_data="return start menu after delivery")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2], [btn_3]])
    return keyboard


def price_kbd():
    btn_1 = types.InlineKeyboardButton(text="Видео-инструкция", url="https://youtu.be/DiH-JkgO6HA")
    btn_2 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="return delivery_cnd after delivery")
    btn_3 = types.InlineKeyboardButton(text="Вернуться в начало", callback_data="return start menu after delivery")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2], [btn_3]])
    return keyboard
