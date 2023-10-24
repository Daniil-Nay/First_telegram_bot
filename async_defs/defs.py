import asyncio
import functools
import aiosqlite
from aiogram import Bot
from aiogram.types import Message
from config_data.config import load_config
from db import DB_get_data, DB_upload_data
import time

config = load_config()
db_path: str = config.db.database_path
bot: Bot = Bot(token=config.tg_bot.token)


def is_admin(func):
    @functools.wraps(func)
    async def wrapped(message: Message, *args, **kwargs):
        is_user_admin = (await DB_get_data())[message.from_user.id]["admin_key"]
        if is_user_admin:
            await func(message, *args, **kwargs)
        else:
            await message.reply("Вы не имеете доступа к этой команде")

    return wrapped


async def distribution(user_id: str, adm_text: str) -> None:
    try:
        await bot.send_message(user_id, adm_text, parse_mode='html')
    except aiosqlite.NotSupportedError as e:
        print(f"Ошибка рассылки уведомления", e)


async def userban(username: str, ban_duration: int) -> None:
    current_time = int(time.time())
    print(current_time)
    end_time = current_time + (ban_duration * 60)
    remaining_time = ban_duration * 60
    while current_time < end_time:
        # print(f"current time {current_time}, end_time {end_time}")
        await DB_upload_data(remaining_time, username, 'blocked_until')
        await asyncio.sleep(10)
        current_time = int(time.time())
        remaining_time = end_time - current_time
        if remaining_time < 0:
            break
    await DB_upload_data(0, username, 'blocked_until')
