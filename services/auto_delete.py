"""Управление сообщениями в чате.

Новая логика:
- при каждом новом действии пользователя предыдущий ответ бота удаляется;
- все сообщения, отправленные в ответ на одно действие, остаются вместе;
- команды пользователя удаляются через DELETE_AFTER_SECONDS,
  если включено DELETE_USER_MESSAGES.
"""

import asyncio

from aiogram import Bot
from aiogram.client.session.middlewares.base import BaseRequestMiddleware
from aiogram.types import CallbackQuery, Message

REPLACE = True
DELETE_AFTER = 2
DELETE_USER = True

# Методы отправки контента — после них запоминаем id сообщений
SEND_METHODS = frozenset({
    'SendMessage', 'SendPhoto', 'SendVideo', 'SendDocument', 'SendAnimation',
    'SendVoice', 'SendAudio', 'SendVideoNote', 'SendSticker', 'SendLocation',
    'SendVenue', 'SendContact', 'SendPoll', 'SendDice', 'SendMediaGroup',
    'CopyMessage',
})

_tasks: set[asyncio.Task] = set()
_last_bot_messages: dict[int | str, list[int]] = {}
_state_lock = asyncio.Lock()
_chat_locks: dict[int | str, asyncio.Lock] = {}


def configure(after_seconds: int = 2,
              user_messages: bool = True,
              replace_messages: bool = True) -> None:
    """Применить настройки, прочитанные из конфига."""
    global DELETE_AFTER, DELETE_USER, REPLACE
    DELETE_AFTER = max(0, int(after_seconds))
    DELETE_USER = bool(user_messages)
    REPLACE = bool(replace_messages)


def _schedule(coro) -> None:
    task = asyncio.create_task(coro)
    _tasks.add(task)
    task.add_done_callback(_tasks.discard)


def _chat_lock(chat_id: int | str) -> asyncio.Lock:
    lock = _chat_locks.get(chat_id)
    if lock is None:
        lock = asyncio.Lock()
        _chat_locks[chat_id] = lock
    return lock


async def _safe_delete(bot: Bot, chat_id: int | str, message_id: int) -> None:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        # Уже удалено, нет прав или истёк срок — игнорируем
        pass


async def _delete_later(bot: Bot, chat_id: int | str, message_id: int) -> None:
    if DELETE_AFTER:
        await asyncio.sleep(DELETE_AFTER)
    await _safe_delete(bot, chat_id, message_id)


async def _drop_previous(bot: Bot, chat_id: int | str) -> None:
    """Удалить сообщения бота из предыдущего действия."""
    if not REPLACE:
        return
    async with _state_lock:
        old_ids = _last_bot_messages.pop(chat_id, [])
    for message_id in old_ids:
        await _safe_delete(bot, chat_id, message_id)


async def _remember(chat_id: int | str, message_ids: list[int | None]) -> None:
    """Запомнить id только что отправленных ботом сообщений."""
    if not REPLACE:
        return
    ids = [mid for mid in message_ids if mid is not None]
    if not ids:
        return
    async with _state_lock:
        _last_bot_messages.setdefault(chat_id, []).extend(ids)


class AutoDeleteMiddleware(BaseRequestMiddleware):
    """Запоминает исходящие сообщения бота для последующей замены."""

    async def __call__(self, make_request, bot: Bot, method):
        result = await make_request(bot, method)
        if type(method).__name__ in SEND_METHODS:
            chat_id = getattr(method, 'chat_id', None)
            if chat_id is not None:
                items = result if isinstance(result, list) else [result]
                await _remember(
                    chat_id,
                    [getattr(item, 'message_id', None) for item in items],
                )
        return result


class DeleteIncomingMiddleware:
    """Перед новым действием убирает старый ответ и команду пользователя."""

    async def __call__(self, handler, event, data):
        bot = data.get('bot') or getattr(event, 'bot', None)

        message = None
        if isinstance(event, Message):
            message = event
        elif isinstance(event, CallbackQuery):
            message = event.message

        chat = getattr(message, 'chat', None)
        chat_id = getattr(chat, 'id', None)

        if bot is None or chat_id is None:
            return await handler(event, data)

        async with _chat_lock(chat_id):
            await _drop_previous(bot, chat_id)
            result = await handler(event, data)
            if DELETE_USER and isinstance(event, Message) and message is not None:
                _schedule(_delete_later(bot, chat_id, message.message_id))
        return result
