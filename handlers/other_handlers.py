import random
from os import getenv
from aiogram import Bot
from aiogram import F
from aiogram.client.session import aiohttp
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message, Sticker
from config_data.config import load_config

r: Router = Router()
config_path = getenv('CONFIG')
config = load_config()
bot: Bot = Bot(token=config.tg_bot.token)


@r.message(Command("cats"))
async def sendcats(message: Message):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.thecatapi.com/v1/images/search'
        async with session.get(url) as cat_response:
            if cat_response.status == 200:
                cat_data = (await cat_response.json())[0]['url']
                await bot.send_photo(message.chat.id, cat_data)
            else:
                await bot.send_message(message.chat.id, 'извините, не удалось отправить фотографию кота')


@r.message(Command("dogs"))
async def senddogs(message: Message):
    async with aiohttp.ClientSession() as session:
        url = 'https://random.dog/woof.json'
        async with session.get(url) as dog_response:
            if dog_response.status == 200:
                dog_data = (await dog_response.json())['url']
                await bot.send_photo(message.chat.id, dog_data)
            else:
                await bot.send_message(message.chat.id, 'извините, не удалось отправить фотографию собаки')


@r.message(Command("secret"))
async def secret_video(message: Message):
    video_url = "https://shattereddisk.github.io/rickroll/rickroll.mp4"
    await bot.send_video(message.chat.id, video=video_url)
    await message.reply(f"<b>{message.chat.first_name}</b>, хаха, вы зарикроленны!", parse_mode="html")


@r.message(F.sticker)
async def send_sticker(message: Sticker):
    try:
        await message.answer_sticker(message.sticker.file_id)
    except Exception as e:
        await message.reply(f"Ошибка отправки стикера в ответ :(", e)


@r.message(F.text.lower().endswith('клоун?') | F.text.lower().endswith('клоунесса?'))
async def wordschecker(message: Message):
    temp_arr = ['да', 'нет', 'скорее нет, чем да']
    expression_1 = f"Я уверен на <b>{random.randint(0, 100)}%</b>, что <b>{random.choice(temp_arr)}</b>"
    await bot.send_message(message.chat.id, expression_1, parse_mode="html")

# для chatgpt
# @r.message()
# async def gpt(message: Message):
#     ai_response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=message.text,
#         temperature=0.5,
#         max_tokens=1000,
#         top_p=1.0,
#         frequency_penalty=0.5,
#         presence_penalty=0.0
#     )
#     await message.reply(ai_response.choices[0].text)
