import aiosqlite
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from db import DB_get_data, table_update
from aiogram.types import Message


class BanMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        try:
            db_data = await DB_get_data()
            try:
                ban_duration = int(db_data[event.chat.id]['ban_duration'])
                if ban_duration != 0:
                    await event.reply("Вы были забанены")
                else:
                    return await handler(event, data)
            except KeyError:
                await table_update(event.from_user.first_name, event.from_user.id)
        except aiosqlite.OperationalError as e:
            print("no such table", e)
            await table_update(event.from_user.first_name,event.from_user.id)
