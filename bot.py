import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from tg_bot.config import load_config

from tg_bot.handlers import start, echo, inline

logger = logging.getLogger(__name__)

config = load_config(path=".env")
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML"))
admins = config.tg_bot.admin_ids


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(message)s')

    # storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(start.router)  # , echo.router inline.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("БОТ ОСТАНОВИЛСЯ!")
