from aiogram import F, Router,types
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Русская кодировка для pdf
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


from aiogram.types import Message, FSInputFile, ChatMemberUpdated, ContentType
from aiogram.filters import Command

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from datetime import datetime, timedelta

router = Router()

#Добовляем админа
from config_data.config import Config, load_config

config: Config = load_config()
admin_ids = config.tg_bot.admin_ids
admin_ids = [admin.lower() for admin in admin_ids]
admin_ids = np.array(admin_ids)

#создание базы данных
# Создание или подключение к базе данных SQLite
conn = sqlite3.connect('./base/telegram_bot_data.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для хранения информации о пользователях
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  last_name TEXT,
                  join_date DATETIME,
                  join_count INTEGER
                  )''')


# Создание таблицы для хранения данных об активности пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS user_activity (
                  user_id INTEGER PRIMARY KEY,
                  activity_date TEXT,
                  activity_count INTEGER
                  )''')

conn.commit()


# Функция для генерации отчета о ежедневной активности пользователей
def generate_daily_activity_report():
    cursor.execute('''SELECT user_id,
                      join_date,
                      join_count
                      FROM users
                      WHERE join_date >= ?
                      GROUP BY user_id''',
                   ((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['user_id', 'join_date', 'join_count'])
    df['join_date'] = pd.to_datetime(df['join_date'])
    df['join_date'] = df['join_date'].dt.date
    return df


# Функция для построения графика активности пользователей
def plot_activity_report(df):
    group_date = df.pivot_table(
    index="join_date", values="join_count", aggfunc="sum"
    )
    plt.figure(figsize=(13, 6))
    sns.barplot(x=group_date.index, y=group_date["join_count"])
    plt.title("Количество новых пользователей за 30 дней")
    plt.xlabel("Дата подключения")
    plt.ylabel("Колличество пользователей")
    plt.grid(True)
    plt.savefig('./base/join_report.png')

# Обработчик команды для запроса отчета
@router.message(Command(commands=['join_report']))
async def send_activity_report(message: Message):
    if message.from_user.username.lower() in admin_ids:
        df = generate_daily_activity_report()
        plot_activity_report(df)
        photo_input = FSInputFile(f'./base/join_report.png')
        await message.answer("Тут отчет о подключенных пользователях за тридцать дней:")
        await message.answer_photo(photo_input)


# Функция для создания PDF-отчета
def generate_pdf_report(df):
    pdfmetrics.registerFont(TTFont('ArialUnicode', './base/ARIALUNI.TTF'))
    plot_activity_report(df)
    photo_input = FSInputFile(f'./base/join_report.png')
    pdf_filename = './base/join_report.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont('ArialUnicode', 12)
    c.drawString(100, 750, 'Отчет о подключенных пользователей')
    c.drawString(100, 730, 'Дата: {}'.format(pd.to_datetime('today').date()))

    # Добавление графика в PDF-отчет
    c.drawImage('./base/join_report.png', 100, 500, width=400, height=300)

    # Добавление таблицы с данными в PDF-отчет
    group_date = df.pivot_table(
    index="join_date", values="join_count", aggfunc="sum"
    )
    group_date['join_date'] = group_date.index
    group_date.columns = ['Количество', 'Дата']
    data = [group_date.columns.values.tolist()] + group_date.values.tolist()
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            c.drawString(200 + j * 80, 500 - (i + 1) * 12, str(val))

    c.showPage()
    c.save()

    return pdf_filename

# Обработчик команды для отправки PDF-отчета\
@router.message(Command(commands=['pdf_report']))
async def send_pdf_report(message: Message):
    if message.from_user.username.lower() in admin_ids:
        df = generate_daily_activity_report()
        pdf_filename = generate_pdf_report(df)
        await message.answer("Тут отчет о подключенных пользователях за семь дней:")
        pdf_file = FSInputFile(f'./base/join_report.pdf')
        await message.answer_document(pdf_file)
