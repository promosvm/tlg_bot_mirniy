from dataclasses import dataclass
from environs import Env

@dataclass
class Tgbot:
    token: str
    admin_ids: None
    weather_token: str

@dataclass
class AutoDelete:
    after_seconds: int
    user_messages: bool
    replace_messages: bool


@dataclass
class Config:
    tg_bot: Tgbot
    auto_delete: AutoDelete

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
        ),
        auto_delete=AutoDelete(
            after_seconds=env.int('DELETE_AFTER_SECONDS', 2),
            user_messages=env('DELETE_USER_MESSAGES', 'true').lower() in ('1', 'true', 'yes'),
            replace_messages=env('REPLACE_BOT_MESSAGES', 'true').lower() in ('1', 'true', 'yes')
        )
    )
