import sqlite3
from aiogram.filters import Command
from aiogram.types import Message
from os import path
from aiogram.dispatcher.router import Router
from lexicon_data import user_info

r: Router = Router()

async def my_start_filter(message: Message) -> bool:
    return message.text == "/start"

@r.message(Command("start"))
async def cmd_start(message: Message):
    root = path.join("C:\\Users\\fff02\\PycharmProjects\\pythonProject1\\db")
    connect = sqlite3.connect(path.join(root, 'users.db'))
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users_info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50)
    )""")
    connect.commit()
    try:
        cursor.execute(f"INSERT INTO users_info(id,name) VALUES (?,?)", (message.chat.id, message.chat.first_name))
        connect.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        cursor.close()
        connect.close()

    await message.reply(text=await user_info(message.chat.first_name, '/start'), parse_mode="html")


async def my_help_filter(message: Message) -> bool:
    return message.text == "/help"


@r.message(my_help_filter)
async def help_message(message: Message):
    await message.reply(text=await user_info(message.chat.first_name,'/help'), parse_mode="html")
