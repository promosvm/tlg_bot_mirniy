from aiogram import F, Router
from keyboards.keyboards import create_inline_kb
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from lexicon.lexicon_ru import LEXICON_MESSAGE, LEXICON_BUTTON_SOUVENIRS 

router = Router()

#Хедлендер отвечающий за начальное меню
@router.callback_query(F.data == 'souvenirs')
async def porcess_start_souvenirs(callback: CallbackQuery):
    keyboard = create_inline_kb(1, last_btn=True, **LEXICON_BUTTON_SOUVENIRS)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/souvenirs'],
        reply_markup=keyboard
    )
    await callback.answer() 

# Этот хедлендер будет срабатывать на сувениры 
@router.callback_query(F.data.in_(LEXICON_BUTTON_SOUVENIRS.keys()))
async def process_all_transport(callback: CallbackQuery):
    image_from_pc = FSInputFile(f'photo/souvenirs/{callback.data}.jpg')
    my_text = open(f'./information_texts/souvenirs/{callback.data}.txt', 'r', encoding='UTF-8')
    text = my_text.read()
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    last_menu = InlineKeyboardButton(text='Назад ⬆️', callback_data='souvenirs')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[last_menu],
                     [main_menu]]
                        )
    await callback.message.answer_photo(image_from_pc, caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()