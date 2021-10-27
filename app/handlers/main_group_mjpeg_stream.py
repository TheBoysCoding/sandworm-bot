import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiohttp import ClientSession

from app.config import config

logger = logging.getLogger(__name__)

async def cmd_mjpeg_stream_photo(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        async with ClientSession() as session:
            async with session.get(f"{config.jpeg_stream.base}?action=snapshot") as response:
                await message.reply_photo(await response.read())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
        logger.exception(f"exception during process message {message}")
    finally:
        await notification_message.delete()

def register_main_group_mjpeg_stream(dp: Dispatcher):
    dp.register_message_handler(cmd_mjpeg_stream_photo, commands="photo2", chat_id=config.telegram.chats)
