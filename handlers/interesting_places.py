from aiogram import F, Router
from keyboards.keyboards import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from lexicon.lexicon_ru import (LEXICON_MESSAGE,
                                LEXICON_BUTTON_INTERESTING_PLACES, 
                                LEXICON_BUTTON_MONUMENTS,
                                LEXICON_BUTTON_MUSEUMS,
                                LEXICON_BUTTON_CHURCH,
                                LEXICON_BUTTON_PARKS)

router = Router()

# Этот хэндлер будет срабатывать на команду "/interesting_places"
@router.callback_query(F.data == 'interesting_places')
async def process_start_inter_places(callback: CallbackQuery):
    keyboard = create_inline_kb(2, last_btn=True, **LEXICON_BUTTON_INTERESTING_PLACES)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/interesting_places'],
        reply_markup=keyboard
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на команду "momuments"
@router.callback_query(F.data == 'monuments')
async def process_start_monuments(callback: CallbackQuery):
    keyboard = create_inline_kb(1, up_btn='interesting_places', last_btn=True, **LEXICON_BUTTON_MONUMENTS)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/monuments'],
        reply_markup=keyboard
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на команду "museums"
@router.callback_query(F.data == 'museums')
async def process_start_museum(callback: CallbackQuery):
    keyboard = create_inline_kb(1, up_btn='interesting_places', last_btn=True, **LEXICON_BUTTON_MUSEUMS)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/museums'],
        reply_markup=keyboard
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на команду "parks"
@router.callback_query(F.data == 'parks')
async def process_start_park(callback: CallbackQuery):
    keyboard = create_inline_kb(1, up_btn='interesting_places', last_btn=True, **LEXICON_BUTTON_PARKS)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/parks'],
        reply_markup=keyboard
    )
    await callback.answer()    


# Этот хэндлер будет срабатывать на команду "temples_and_churches"
@router.callback_query(F.data == 'temples_and_churches')
async def process_start_church(callback: CallbackQuery):
    keyboard = create_inline_kb(1, up_btn='interesting_places', last_btn=True, **LEXICON_BUTTON_CHURCH)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/temples_and_churches'],
        reply_markup=keyboard
    )
    await callback.answer()


# Этот хедлендер будет срабатывать на инересные места
@router.callback_query(F.data.in_(LEXICON_BUTTON_MONUMENTS.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_MUSEUMS.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_CHURCH.keys()))
@router.callback_query(F.data.in_(LEXICON_BUTTON_PARKS.keys()))
async def process_start_other_places(callback: CallbackQuery):
    image_from_pc = FSInputFile(f'photo/interesting_places/{callback.data}.jpg')
    my_text = open(f'./information_texts/interesting_places/{callback.data}.txt', 'r', encoding='UTF-8')
    text = my_text.read()
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    #делаем кнопку назад для каждого меню
    if callback.data in LEXICON_BUTTON_MONUMENTS.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='monuments')
    if callback.data in LEXICON_BUTTON_MUSEUMS.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='museums')
    if callback.data in LEXICON_BUTTON_CHURCH.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='temples_and_churches')
    if callback.data in LEXICON_BUTTON_PARKS.keys():
        last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='parks')               
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(image_from_pc, caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()
