import asyncio
from os import getenv

from aiogram import Bot
from aiogram import Dispatcher

from config_data.config import load_config
from handlers import user_handlers, other_handlers




async def main():
    config_path = getenv('CONFIG')
    config = load_config(config_path)
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    dp.include_router(user_handlers.r)
    dp.include_router(other_handlers.r)

    # await send_to_users() #функция отправки уведомлений пользователям, которые есть в бд

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
