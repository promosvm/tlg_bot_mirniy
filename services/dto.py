"""Универсальные DTO: не зависят ни от Telegram, ни от Max."""

import math
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple


class ContentItem(NamedTuple):
    """Контент локации: путь к фото и текст описания."""

    photo_path: str
    text: str


@dataclass(frozen=True)
class UserData:
    """Данные пользователя, пришедшие из мессенджера."""

    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    join_date: datetime


@dataclass(frozen=True)
class WeatherData:
    """Нормализованные данные погоды + их текстовое представление."""

    temperature: int
    feels_like: int
    description: str
    humidity: int
    pressure_mm: int
    wind_speed: int

    @classmethod
    def from_api(cls, payload: dict) -> "WeatherData":
        """Преобразует ответ OpenWeatherMap в DTO."""
        main = payload["main"]
        return cls(
            temperature=round(main["temp"]),
            feels_like=round(main["feels_like"]),
            description=payload["weather"][0]["description"],
            humidity=main["humidity"],
            pressure_mm=math.ceil(main["pressure"] / 1.333),
            wind_speed=round(payload["wind"]["speed"]),
        )

    def as_text(self) -> str:
        """Возвращает готовое сообщение (одинаково для любой платформы)."""
        return (
            f"СЕГОДНЯ:\n\n🌬 {self.description}\n"
            f"🌡️ температура: {self.temperature}°C, ощущается как {self.feels_like}°C \n"
            f"💧 влажность: {self.humidity}%\n"
            f"♨️ давление: {self.pressure_mm} мм.рт.ст\n"
            f"༄   ветер: {self.wind_speed} м/с \n\n"
            f"Хорошего дня 😎!"
        )
