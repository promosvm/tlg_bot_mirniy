import requests
import datetime
import math
from aiogram import F, Router
from aiogram.types import  CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config_data.config import Config, load_config

#загружаем токен для погоды
config: Config = load_config()
WEATHER_TOKEN = config.tg_bot.weather_token
print(WEATHER_TOKEN)
router = Router()


@router.callback_query(F.data == 'weather_today')
async def procees_get_weather(callback: CallbackQuery):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat=62.7641&lon=40.3375&exclude=minute&&lang=ru&units=metric&appid={WEATHER_TOKEN}')
    data = response.json()
    cur_temp = data["main"]["temp"]
    feels_temp = data['main']['feels_like']
    weather = data['weather'][0][ 'description']
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[main_menu]])
    await callback.message.answer(text = f"СЕГОДНЯ:\n\n🌬 {weather}\n"
        f"🌡️ температура: {round(cur_temp)}°C, ощущается как {round(feels_temp)}°C \n"
        f'💧 влажность: {humidity}%\n♨️ давление: {math.ceil(pressure/1.333)} мм.рт.ст\n༄   ветер: {round(wind)} м/с \n\n'
        f'Хорошего дня 😎!',
        reply_markup=keyboard)
    await callback.answer()
