from dataclasses import dataclass
from os import getenv

import openai
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str = None) -> Config:
    load_dotenv()
    bot_key = getenv("API_chatbot_KEY")
    openai.api_key = getenv("API_openai_KEY")
    return Config(tg_bot=TgBot(token=bot_key,
                               admin_ids=list(map(int, getenv("ADMIN_IDS")))),
                  db=DatabaseConfig(database=getenv("DATABASE"),
                                    db_host=getenv('DB_HOST'),
                                    db_user=getenv('DB_USER'),
                                    db_password=getenv('DB_PASSWORD')))
