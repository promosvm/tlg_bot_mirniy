from aiogram import F, Router
from services.keyboard import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from services.text import LEXICON_MESSAGE, LEXICON_BUTTON_SOUVENIRS 
from services.content import get_content

router = Router()

#Хэндлер отвечающий за начальное меню
@router.callback_query(F.data == 'souvenirs')
async def porcess_start_souvenirs(callback: CallbackQuery):
    keyboard = create_inline_kb(1, last_btn=True, **LEXICON_BUTTON_SOUVENIRS)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/souvenirs'],
        reply_markup=keyboard
    )
    await callback.answer() 

# Этот хэндлер будет срабатывать на сувениры 
@router.callback_query(F.data.in_(LEXICON_BUTTON_SOUVENIRS.keys()))
async def process_all_transport(callback: CallbackQuery):
    photo_path, text = get_content('souvenirs', callback.data)
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='souvenirs')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(FSInputFile(photo_path), caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()
