# import sqlite3
#
# import aiogram
# from aiogram.types import Message
# from aiogram import Dispatcher,Bot
# from os import path
# import random
# import time
#
# async def quote_evrday(chat_id):  # WIP
#     message = "testquote"
#     mins = 1
#     mins = 60 * int(mins)
#     time.sleep(mins)
#     await bot.send_message(chat_id, message)
#
#
# async def notification_info(chat_id):
#     message = "testquote"  # для уведомления пользователей из БД
#     await bot.send_message(chat_id, message, parse_mode="html")
#
#
# async def send_to_users():
#     root = path.dirname(path.realpath(__file__))
#     connect = sqlite3.connect(path.join(root, 'users.db'))  # feauters_test/users.db
#     cursor = connect.cursor()
#     cursor.execute("SELECT id FROM users_info")
#     chat_ids = cursor.fetchall()
#     connect.close()
#     cids = [chat_id[0] for chat_id in chat_ids]
#     for chat_id in cids:
#         try:
#             # await quote_evrday(chat_id)
#             await notification_info(chat_id)
#         except aiogram.exceptions.RetryAfter as e:
#             print(f"Ошибка отправки тестового сообщения")
#
