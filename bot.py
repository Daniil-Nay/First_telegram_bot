import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from config_data.config import load_config
from handlers import user_handlers, other_handlers, admin_handlers
from middlewares import BanMiddleware


async def main():
    config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    dp.message.middleware.register(BanMiddleware())
    dp.include_router(user_handlers.r)
    dp.include_router(other_handlers.r)
    dp.include_router(admin_handlers.r)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
