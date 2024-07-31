import asyncio

from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def echo(message: Message):
    # await message.answer(message.text)

    # Удалить сообщение пользователя
    # await message.reply("Это сообщение удалится через 3 секунды.")
    # await asyncio.sleep(3)
    # await message.delete()

    # Удалить ответное сообщение бота
    # bots_msg = await message.reply("Это сообщение удалится через 3 секунды.")
    # await asyncio.sleep(3)
    # await bots_msg.delete()

    # Редактировать сообщение
    bots_msg = await message.reply("Это сообщение удалится через 5...")
    i = 4
    while i >= 0:
        await asyncio.sleep(1)
        await bots_msg.edit_text(f"Это сообщение удалится через {i}...")
        i -= 1
    await bots_msg.delete()
    await message.delete()
