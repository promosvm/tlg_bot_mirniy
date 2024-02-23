from aiogram import F, Router
from keyboards.keyboards import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from lexicon.lexicon_ru import (LEXICON_BUTTON_BUS, 
                                LEXICON_BUTTON_TRANSPORT,
                                LEXICON_MESSAGE)

router = Router()

# Этот хэндлер будет срабатывать на команду "/transport_town"
@router.callback_query(F.data == 'transport_town')
async def process_transport_town(callback: CallbackQuery):
    keyboard = create_inline_kb(2, last_btn=True, **LEXICON_BUTTON_TRANSPORT)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/transport'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "bus"
@router.callback_query(F.data == 'bus')
async def process_bus(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='transport_town', last_btn=True, **LEXICON_BUTTON_BUS)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/bus'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хедлендер будет срабатывать на транспорт
@router.callback_query(F.data.in_(LEXICON_BUTTON_BUS.keys()))
@router.callback_query(F.data == 'taxi')
async def process_all_transport(callback: CallbackQuery):
    image_from_pc = FSInputFile(f'photo/transport/{callback.data}.jpg')
    my_text = open(f'./information_texts/transport/{callback.data}.txt', 'r', encoding='UTF-8')
    text = my_text.read()
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='bus')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(image_from_pc, caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()

