from aiogram import F, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

router = Router()

# Хэндлер для сообщений о мне
@router.callback_query(F.data == 'about_me')
async def process_start_monuments(callback: CallbackQuery):
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[main_menu]]
                        )
    await callback.message.answer(
        text=f'Вся информация, указанная в боте, носит ознакомительный характер,не является рекламой!\n'
            'Вы заметили ошибки?\n'
            'Пожалуйста напишите мне info@botorobot.ru',
        reply_markup=keyboard
    )
    await callback.answer()
