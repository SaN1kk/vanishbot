from aiogram import types
from aiogram.fsm.state import StatesGroup, State


def cancel_settings():
    btn_1 = types.InlineKeyboardButton(text="Отмена", callback_data="cancel settings")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[btn_1]])
    return keyboard


class WaitingSettings(StatesGroup):
    waiting_settings = State()
