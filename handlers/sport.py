from aiogram import F, Router
from keyboards.keyboards import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from lexicon.lexicon_ru import (LEXICON_BUTTON_SPORT,
                                LEXICON_MESSAGE)

router = Router()


# Этот хэндлер будет срабатывать на команду "/hotel"
@router.callback_query(F.data == 'sport')
async def process_start_inter_places(callback: CallbackQuery):
    keyboard = create_inline_kb(1, last_btn=True, **LEXICON_BUTTON_SPORT)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/sport'],
        reply_markup=keyboard
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на все что есть в отелях
@router.callback_query(F.data.in_(LEXICON_BUTTON_SPORT.keys()))
async def process_all_transport(callback: CallbackQuery):
    image_from_pc = FSInputFile(f'photo/sport/{callback.data}.jpg')
    my_text = open(f'./information_texts/sport/{callback.data}.txt', 'r', encoding='UTF-8')
    text = my_text.read()
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='sport')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(image_from_pc, caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()
