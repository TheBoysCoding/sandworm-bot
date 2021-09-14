__all__ = ("bot", "dp", "notify_message", "notify_sticker")

import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from .config import config

bot = Bot(token=config.telegram.token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

log = logging.getLogger(__name__)

def get_notify_chats():
    yield from config.telegram.chats

async def notify_message(text: str):
    for chat_id in get_notify_chats():
        try:
            await bot.send_message(chat_id, text)
        except:
            log.exception(f"failed to send message to chat_id={chat_id}")


async def notify_sticker(sticker_id: str):
    for chat_id in get_notify_chats():
        try:
            await bot.send_sticker(chat_id, sticker_id)
        except:
            log.exception(f"failed to send sticker to chat_id={chat_id}")


