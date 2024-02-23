from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

router = Router()

# Этот хедлендер будет срабатывать на эксренные службы
@router.callback_query(F.data == 'emergency')
async def process_all_transport(callback: CallbackQuery):
    image_from_pc = FSInputFile(f'photo/emergency/{callback.data}.jpg')
    my_text = open(f'./information_texts/emergency/{callback.data}.txt', 'r', encoding='UTF-8')
    text = my_text.read()
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[main_menu]])
    await callback.message.answer_photo(image_from_pc, caption=text, parse_mode='HTML', reply_markup=keyboard)
    await callback.answer()