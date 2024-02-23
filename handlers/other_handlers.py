from aiogram import F, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

router = Router()

# Хэндлер для сообщений, j,hfnyjq cdzpb 
@router.callback_query(F.data == 'about_me')
async def process_start_monuments(callback: CallbackQuery):
    main_menu = InlineKeyboardButton(text='Главное меню 🔁', callback_data='main_menu')
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[main_menu]]
                        )
    await callback.message.answer(
        text=f'Вы заметили ошибки? \n'
            'Пожалуйста напишите мне @mylogloss',
        reply_markup=keyboard
    )
    await callback.answer()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
# @router.message()
# async def send_answer(message: Message):
#     await message.answer(text=f'Извините, но я не понимаю команду {message.text}.'
#                          'Пожалуйста, попробуйте еще раз или воспользуйтесь командой /help ' 
#                          'для получения дополнительной информации о доступных командах')
    