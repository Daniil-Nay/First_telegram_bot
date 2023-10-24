from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router

from lexicon_data import user_info
from db import table_update, DB_get_data

r: Router = Router()


@r.message(Command("start"))
async def cmd_start(message: Message):
    data = await DB_get_data()
    # await table_update(message.from_user.first_name, message.from_user.id)
    try:
        user_data = data[message.from_user.id]
        command = '/admin_start' if user_data['admin_key'] else '/help'
    except KeyError:
        command = '/start'
    await message.reply(text=await user_info(message.from_user.first_name, command), parse_mode="html")


@r.message(Command("help"))
async def help_message(message: Message):
    data = await DB_get_data()
    try:
        user_data = data[message.from_user.id]
        command = '/admin_help' if user_data['admin_key'] else '/help'
    except KeyError:
        command = '/help'

    await message.reply(text=await user_info(message.from_user.first_name, command), parse_mode="html")

