import array
import asyncio
from aiogram import Router
from config_data.config import load_config
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from async_defs import is_admin, distribution, userban
from db import DB_get_data, DB_upload_data

r: Router = Router()
config = load_config()
db_path: str = config.db.database_path


class AdminStates(StatesGroup):
    ban_time = State()
    waiting_for_text = State()
    writing_the_nickname = State()
    writing_the_nickname2 = State()
    whom_to_ban = State()


@r.message(Command("notify"))
@is_admin
async def notification_details(message: Message, state: FSMContext) -> None:
    await message.reply("Напишите текст для уведомления пользователей:")
    await state.set_state(AdminStates.waiting_for_text)


@r.message(AdminStates.waiting_for_text)
async def send_to_users(message: Message, state: FSMContext) -> None:
    global db_path
    users_data: tuple = tuple((await DB_get_data()).keys())
    adm_text: str = f"Пишет владелец бота:\n{message.text}"
    tasks = [distribution(user_id, adm_text) for user_id in users_data]
    await asyncio.gather(*tasks)
    await state.clear()


@r.message(Command("promote"))
@is_admin
async def user_promotion(message: Message, state: FSMContext) -> None:
    nicknames: list = list(data['username'] for data in (await DB_get_data()).values())
    try:
        await message.reply(f"Напишите ник пользователя, которому хотите расширить увеличить набор команд.\n"
                            f"Пользователи: {', '.join(nicknames)}")
        await state.set_state(AdminStates.writing_the_nickname)
    except Exception as e:
        await message.reply(f"Ошибка, {e}")
        raise


@r.message(AdminStates.writing_the_nickname)
async def user_promotion(message: Message, state: FSMContext) -> None:
    users_data: array = list(data['username'] for data in (await DB_get_data()).values())
    if message.text in users_data:
        await DB_upload_data(1, str(message.text), 'is_admin')
        await message.reply(f"Пользователь <b>{message.text}</b> повышен до админа", parse_mode="html")
    else:
        await message.reply(f"Ошибка, данного пользователя нет в списке")
        raise
    await state.clear()


@r.message(Command("demote"))
@is_admin
async def user_demotion(message: Message, state: FSMContext) -> None:
    nicknames: list = list(data['username'] for data in (await DB_get_data()).values())
    try:
        await message.reply("Напишите ник пользователя, которому хотите уменьшить набор команд.\n"
                            f"Пользователи: {', '.join(nicknames)}")
        await state.set_state(AdminStates.writing_the_nickname2)
    except Exception as e:
        await message.reply(f"Ошибка, {e}")
        raise


@r.message(AdminStates.writing_the_nickname2)
async def user_demotion(message: Message, state: FSMContext) -> None:
    print("i am inm")
    users_data: list = list(data['username'] for data in (await DB_get_data()).values())
    if message.text in users_data:
        await DB_upload_data(0, str(message.text), 'is_admin')
        await message.reply(f"Пользователь <b>{message.text}</b> понижен до обычного пользователя", parse_mode="html")
    else:
        await message.reply(f"Ошибка, данного пользователя нет в списке")
    await state.clear()


@r.message(Command("ban"))
@is_admin
async def user_ban(message: Message, state: FSMContext) -> None:
    nicknames: list = list(data['username'] for data in (await DB_get_data()).values())
    print(await DB_get_data())
    await message.reply("Напишите ник пользователя, которого хотите забанить.\n"
                        f"Пользователи: {', '.join(nicknames)}")
    await state.set_state(AdminStates.whom_to_ban)


@r.message(AdminStates.whom_to_ban)
async def user_ban(message: Message, state: FSMContext) -> None:
    await message.reply("Введите время (в мин) для бана")
    await state.update_data(ctext=message.text)
    await state.set_state(AdminStates.ban_time)


@r.message(AdminStates.ban_time)
async def user_ban(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    # print(f"State data {data.get('ctext')}")
    duration: int = int(message.text)
    await userban(data.get('ctext'), duration)
    await state.clear()
