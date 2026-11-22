import os
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_daily_activity_report() -> list:
    """Формирует DataFrame с пользователями за последние 30 дней."""
    import sqlite3
    from services.database import get_connection

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT user_id, join_date, join_count
           FROM users
           WHERE join_date >= ?''',
        ((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),),
    )
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['user_id', 'join_date', 'join_count'])
    df['join_date'] = pd.to_datetime(df['join_date'])
    df['join_date'] = df['join_date'].dt.date
    return df


def plot_activity_report(df) -> str:
    """Строит график и сохраняет его в ./base/join_report.png."""
    group_date = df.pivot_table(index="join_date", values="join_count", aggfunc="sum")
    plt.figure(figsize=(13, 6))
    sns.barplot(x=group_date.index, y=group_date["join_count"])
    plt.title("Количество новых пользователей за 30 дней")
    plt.xlabel("Дата подключения")
    plt.ylabel("Колличество пользователей")
    plt.grid(True)
    plt.savefig('./base/join_report.png')
    return './base/join_report.png'


def generate_pdf_report(df) -> str:
    """Генерирует PDF-отчёт и возвращает путь к файлу."""
    pdfmetrics.registerFont(TTFont('ArialUnicode', './base/ARIALUNI.TTF'))
    plot_activity_report(df)
    pdf_filename = './base/join_report.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont('ArialUnicode', 12)
    c.drawString(100, 750, 'Отчет о подключенных пользователях')
    c.drawString(100, 730, 'Дата: {}'.format(pd.to_datetime('today').date()))

    group_date = df.pivot_table(index="join_date", values="join_count", aggfunc="sum")
    group_date['join_date'] = group_date.index
    group_date.columns = ['Количество', 'Дата']
    data = [group_date.columns.values.tolist()] + group_date.values.tolist()
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            c.drawString(200 + j * 80, 500 - (i + 1) * 12, str(val))

    c.showPage()
    c.save()
    return pdf_filename
