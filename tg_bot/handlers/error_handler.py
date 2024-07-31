import logging

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest, TelegramAPIError

router = Router()


@router.error()
async def errors_handler(update, exception):
    if isinstance(exception, TelegramBadRequest):
        logging.exception(f"Ошибка: Не может распознать сущности сообщения. \nАпдейт: {update}")
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f"Ошибка: Telegram API. \nАпдейт: {update}")
        return True

    logging.exception(f"Ошибка: {exception}. \nАпдейт: {update}")
