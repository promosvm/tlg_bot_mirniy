import requests

from config_data.config import Config, load_config
from services.dto import WeatherData

config: Config = load_config()
WEATHER_TOKEN = config.tg_bot.weather_token


def fetch_weather(lat: float = 62.7641, lon: float = 40.3375, appid: str = None) -> dict:
    """Возвращает сырой ответ OpenWeatherMap."""
    token = appid or WEATHER_TOKEN
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}'
        f'&exclude=minute&&lang=ru&units=metric&appid={token}'
    )
    return response.json()


def get_weather(lat: float = 62.7641, lon: float = 40.3375, appid: str = None) -> WeatherData:
    """Возвращает нормализованные данные погоды (DTO)."""
    return WeatherData.from_api(fetch_weather(lat, lon, appid))
