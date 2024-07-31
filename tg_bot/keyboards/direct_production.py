from aiogram import types


def direct_production():
    btn_1 = types.InlineKeyboardButton(text="Бесплатная консультация", callback_data="free consultation")
    btn_2 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="return start menu")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2]])
    return keyboard

