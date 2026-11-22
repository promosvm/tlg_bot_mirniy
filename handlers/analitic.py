from aiogram import F, Router, types
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
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

from services.database import get_connection, init_db
from services.report import generate_daily_activity_report, plot_activity_report, generate_pdf_report

router = Router()

#Добовляем админа
from config_data.config import Config, load_config

config: Config = load_config()
admin_ids = config.tg_bot.admin_ids
admin_ids = [admin.lower() for admin in admin_ids]
admin_ids = np.array(admin_ids)

#создание базы данных
init_db(get_connection())


# Обработчик команды для запроса отчета
@router.message(Command(commands=['join_report']))
async def send_activity_report(message: Message):
    if message.from_user.username.lower() in admin_ids:
        df = generate_daily_activity_report()
        plot_activity_report(df)
        photo_input = FSInputFile(f'./base/join_report.png')
        await message.answer("Тут отчет о подключенных пользователях за тридцать дней:")
        await message.answer_photo(photo_input)


# Обработчик команды для отправки PDF-отчета
@router.message(Command(commands=['pdf_report']))
async def send_pdf_report(message: Message):
    if message.from_user.username.lower() in admin_ids:
        df = generate_daily_activity_report()
        pdf_filename = generate_pdf_report(df)
        await message.answer("Тут отчет о подключенных пользователях за семь дней:")
        pdf_file = FSInputFile(f'./base/join_report.pdf')
        await message.answer_document(pdf_file)
