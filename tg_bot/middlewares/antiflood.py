from datetime import timedelta, datetime
from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

user_last_execution: Dict[int, datetime] = {}
COOLDOWN_PERIOD = timedelta(seconds=5)


class AntiFloodMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        now = datetime.now()

        if user_id in user_last_execution:
            last_execution_time = user_last_execution[user_id]

            time_since_last_execution = now - last_execution_time
            pause = int(COOLDOWN_PERIOD.total_seconds() - time_since_last_execution.total_seconds())
            if pause > 0:
                await event.answer(
                    f"Подождите <b>{pause} сек</b> перед повторной отправкой."
                )
                return

        user_last_execution[user_id] = now

        return await handler(event, data)
