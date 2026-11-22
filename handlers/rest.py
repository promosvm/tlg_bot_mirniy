from aiogram import F, Router
from services.keyboard import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from services.text import (LEXICON_MESSAGE, 
                                LEXICON_BUTTON_REST,
                                LEXICON_BUTTON_CINEMA,
                                LEXICON_BUTTON_BILLIARD,
                                LEXICON_BUTTON_WASH,
                                LEXICON_BUTTON_NIGHT_CLUB) 
from services.content import get_content

router = Router()

#Хедлендер отвечающий за начальное меню
@router.callback_query(F.data == 'rest')
async def porcess_start_rest(callback: CallbackQuery):
    keyboard = create_inline_kb(2, last_btn=True, **LEXICON_BUTTON_REST)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/rest'],
        reply_markup=keyboard
    )
    await callback.answer() 

# Этот хэндлер будет срабатывать на команду "wash"
@router.callback_query(F.data == 'wash')
async def process_start_church(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='rest', last_btn=True, **LEXICON_BUTTON_WASH)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/wash'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "cinema"
@router.callback_query(F.data == 'cinema')
async def process_start_church(callback: CallbackQuery):
    keyboard = create_inline_kb(1, up_btn='rest', last_btn=True, **LEXICON_BUTTON_CINEMA)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/cinema'],
        reply_markup=keyboard
    )
    await callback.answer()    

# Этот хэндлер будет срабатывать на команду "billiard"
@router.callback_query(F.data == 'billiard')
async def process_start_church(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='rest', last_btn=True, **LEXICON_BUTTON_BILLIARD)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/billiard'],
        reply_markup=keyboard
    )
    await callback.answer() 
    
# Этот хэндлер будет срабатывать на команду "night_club"
@router.callback_query(F.data == 'night_club')
async def process_start_church(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='rest', last_btn=True, **LEXICON_BUTTON_NIGHT_CLUB)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/night_club'],
        reply_markup=keyboard
    )
    await callback.answer() 

# Этот хедлендер будет срабатывать на все что в отдыхе 
@router.callback_query(F.data.in_(LEXICON_BUTTON_REST))
@router.callback_query(F.data.in_(LEXICON_BUTTON_CINEMA))
@router.callback_query(F.data.in_(LEXICON_BUTTON_BILLIARD))
@router.callback_query(F.data.in_(LEXICON_BUTTON_WASH))
@router.callback_query(F.data.in_(LEXICON_BUTTON_NIGHT_CLUB))
async def process_all_transport(callback: CallbackQuery):
    photo_path, text = get_content('rest', callback.data)
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    if callback.data in LEXICON_BUTTON_CINEMA.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='cinema')    
    if callback.data in LEXICON_BUTTON_REST.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='rest')
    if callback.data in LEXICON_BUTTON_BILLIARD.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='billiard')
    if callback.data in LEXICON_BUTTON_WASH.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='wash') 
    if callback.data in LEXICON_BUTTON_NIGHT_CLUB.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='night_club')                          
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(FSInputFile(photo_path), caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer() 
