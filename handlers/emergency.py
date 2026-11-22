from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from services.content import get_content

router = Router()

# Этот хэндлер будет срабатывать на экстренные службы
@router.callback_query(F.data == 'emergency')
async def process_all_transport(callback: CallbackQuery):
    photo_path, text = get_content('emergency', callback.data)
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[main_menu]])
    await callback.message.answer_photo(FSInputFile(photo_path), caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()
