from aiogram import F, Router
from services.keyboard import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from services.text import (LEXICON_MESSAGE,
                                LEXICON_BUTTON_LOCAL_CUISENE, 
                                LEXICON_BUTTON_CAFE,
                                LEXICON_BUTTON_DELIVERY,
                                LEXICON_BUTTON_RESTORAN,
                                LEXICON_BUTTON_COFFE,
                                LEXICON_BUTTON_LOCAL_FAST_FOOD)
from services.content import get_content

router = Router()

# Этот хэндлер будет срабатывать на команду "/local_cuisine"
@router.callback_query(F.data == 'local_cuisine')
async def process_start_inter_places(callback: CallbackQuery):
    keyboard = create_inline_kb(2, last_btn=True, **LEXICON_BUTTON_LOCAL_CUISENE)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/local_cuisine'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "cafe"
@router.callback_query(F.data == 'cafe')
async def process_start_monuments(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='local_cuisine', last_btn=True, **LEXICON_BUTTON_CAFE)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/cafe'],
        reply_markup=keyboard
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на команду "delivery"
@router.callback_query(F.data == 'delivery')
async def process_start_museum(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='local_cuisine', last_btn=True, **LEXICON_BUTTON_DELIVERY)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/delivery'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "restoran"
@router.callback_query(F.data == 'restoran')
async def process_start_park(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='local_cuisine', last_btn=True, **LEXICON_BUTTON_RESTORAN)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/restoran'],
        reply_markup=keyboard
    )
    await callback.answer()    

# Этот хэндлер будет срабатывать на команду "coffe"
@router.callback_query(F.data == 'coffe')
async def process_start_church(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='local_cuisine', last_btn=True, **LEXICON_BUTTON_COFFE)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/coffe'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "fastfood"
@router.callback_query(F.data == 'fast_food')
async def process_start_monuments(callback: CallbackQuery):
    keyboard = create_inline_kb(2, up_btn='local_cuisine', last_btn=True, **LEXICON_BUTTON_LOCAL_FAST_FOOD)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/fast_food'],
        reply_markup=keyboard
    )
    await callback.answer()



# Этот хэндлер будет срабатывать на инeresting места
@router.callback_query(F.data.in_(LEXICON_BUTTON_CAFE.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_DELIVERY.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_RESTORAN.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_COFFE.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_LOCAL_FAST_FOOD.keys()))
async def process_start_other_places(callback: CallbackQuery):
    photo_path, text = get_content('local_cuisine', callback.data)
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    #делаем кнопку назад для каждого меню
    if callback.data in LEXICON_BUTTON_CAFE.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='cafe')
    if callback.data in LEXICON_BUTTON_DELIVERY.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='delivery')
    if callback.data in LEXICON_BUTTON_RESTORAN.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='restoran')
    if callback.data in LEXICON_BUTTON_COFFE.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='coffe')
    if callback.data in LEXICON_BUTTON_LOCAL_FAST_FOOD.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='fast_food')                 
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(FSInputFile(photo_path), caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()
