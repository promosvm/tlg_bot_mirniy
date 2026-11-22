from aiogram import F, Router
from services.keyboard import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from services.text import (LEXICON_BUTTON_HOTEL, LEXICON_MESSAGE)
from services.content import get_content

router = Router()

# Этот хэндлер будет срабатывать на команду "/hotel"
@router.callback_query(F.data == 'hotel')
async def process_start_inter_places(callback: CallbackQuery):
    keyboard = create_inline_kb(2, last_btn=True, **LEXICON_BUTTON_HOTEL)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/hotel'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на все что есть в отелях
@router.callback_query(F.data.in_(LEXICON_BUTTON_HOTEL.keys()))
async def process_all_transport(callback: CallbackQuery):
    photo_path, text = get_content('hotel', callback.data)
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='hotel')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[last_menu],
                         [main_menu]]
                        )
    await callback.message.answer_photo(FSInputFile(photo_path), caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()
