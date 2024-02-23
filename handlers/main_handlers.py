from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import create_inline_kb
from lexicon.lexicon_ru import (LEXICON_MESSAGE, LEXICON_BUTTON_MAIN)

import sqlite3

router = Router()

#подключаемся к базе данных
conn = sqlite3.connect('./base/telegram_bot_data.db', check_same_thread=False)
cursor = conn.cursor()


# Этот хэндлер будет срабатывать на команду "/start" + добавлять данные по пользователю в базу данных
# и отправлять в чат клавиатуру
@router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(2, **LEXICON_BUTTON_MAIN)
    # Добовляем пользователя в базу
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    join_date = message.date
    # Проверяем, есть ли пользователь уже в базе данных
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user is None:
         cursor.execute('''INSERT INTO users
                           (user_id, username, first_name, last_name, join_date, join_count)
                           VALUES (?, ?, ?, ?, ?, 1)''',
                            (user_id, username, first_name, last_name, join_date))
         conn.commit()
        #  conn.close()

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
