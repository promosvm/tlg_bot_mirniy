import os

from services.dto import ContentItem


def get_photo_path(category: str, key: str) -> str:
    """Возвращает путь до фото локации/объекта."""
    return f'./photo/{category}/{key}.jpg'


def get_text(category: str, key: str) -> str:
    """Читает текст о местности/объекте из файла информации_texts."""
    with open(f'./information_texts/{category}/{key}.txt', 'r', encoding='UTF-8') as f:
        return f.read()


def get_content(category: str, key: str) -> ContentItem:
    """Возвращает DTO с фото и текстом (распаковывается как кортеж)."""
    return ContentItem(
        photo_path=get_photo_path(category, key),
        text=get_text(category, key),
    )
