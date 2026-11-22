from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from services.weather import get_weather

router = Router()


@router.callback_query(F.data == 'weather_today')
async def procees_get_weather(callback: CallbackQuery):
    # Бизнес-логика и форматирование — в сервисе/DTO
    data = get_weather()
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[main_menu]])
    await callback.message.answer(text=data.as_text(), reply_markup=keyboard)
    await callback.answer()
