from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from services.keyboard import create_inline_kb
from services.text import (LEXICON_MESSAGE, LEXICON_BUTTON_MAIN)
from services.database import get_connection, add_user
from services.dto import UserData

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" + добавлять данные по пользователю в базу данных
# и отправлять в чат клавиатуру
@router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(2, **LEXICON_BUTTON_MAIN)
    # Добовляем пользователя в базу через сервис
    conn = get_connection()
    user = UserData(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        join_date=message.date,
    )
    add_user(conn=conn, user=user)
    await message.answer(
        text=LEXICON_MESSAGE['/start'],
        reply_markup=keyboard
    )


@router.callback_query(F.data.in_(['main_menu']))
async def process_start__other(callback: CallbackQuery):
    keyboard = create_inline_kb(2, **LEXICON_BUTTON_MAIN)
    await callback.message.answer(
        text=LEXICON_MESSAGE['/start'],
        reply_markup=keyboard
    )
    await callback.answer()
