from dataclasses import dataclass
from environs import Env

@dataclass
class Tgbot:
    token: str
    admin_ids: None
    weather_token: str

@dataclass
class Config:
    tg_bot: Tgbot

# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=Tgbot(
            token=env('BOT_TOKEN'),
            admin_ids = env('ADMIN_IDS').split(', '),
            weather_token=env('WEATHER_TOKEN')
        )
    )
