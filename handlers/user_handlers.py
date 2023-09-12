from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router
from lexicon_data import user_info
from db import table_update
r: Router = Router()


@r.message(Command("start"))
async def cmd_start(message: Message):
    await table_update(message.chat.id, message.chat.first_name)
    await message.reply(text=await user_info(message.chat.first_name, '/start'), parse_mode="html")


@r.message(Command("help"))
async def help_message(message: Message):
    await message.reply(text=await user_info(message.chat.first_name,'/help'), parse_mode="html")
