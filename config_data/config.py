from dataclasses import dataclass
from os import getenv

import openai
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    database_path: str


@dataclass
class TgBot:
    token: str
    ai_key: str
    creator_id: int

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config() -> Config:
    load_dotenv()
    # openai.api_key = getenv("API_openai_KEY")
    return Config(tg_bot=TgBot(token=getenv("API_chatbot_KEY"),
                               ai_key = getenv("API_openai_KEY"),
                               creator_id = int(getenv("CREATOR_ID"))),
                  db=DatabaseConfig(database_path=getenv("DATABASE_path")))


