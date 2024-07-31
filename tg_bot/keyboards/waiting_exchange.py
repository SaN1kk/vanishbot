from aiogram import types
from aiogram.fsm.state import StatesGroup, State


def exchange_kbd():
    btn_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="return start menu after exchange")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1]])
    return keyboard


def confirm_keyboard():
    btn_1 = types.InlineKeyboardButton(text="Да", callback_data="confirm exchange")
    btn_2 = types.InlineKeyboardButton(text="Нет", callback_data="cancel exchange")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1, btn_2]])
    return keyboard


class Waiting(StatesGroup):
    waiting_exchange = State()
