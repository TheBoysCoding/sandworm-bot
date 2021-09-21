import asyncio
import logging

from aiogram.types import Message

from app.core import dp
from app.config import config
from app.misc import Camera

log = logging.getLogger(__name__)

camera = Camera(device=config.camera.device)

@dp.message_handler(commands="photo", chat_id=config.telegram.chats)
async def command_handler_photo(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        await message.reply_photo(await camera.capture_photo())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
    finally:
        await notification_message.delete()

@dp.message_handler(commands="video", chat_id=config.telegram.chats)
async def command_handler_video(message: Message):
    duration_str = message.get_args()

    if duration_str:
        try:
            duration = int(duration_str)
        except (ValueError, TypeError):
            return await message.reply("\N{Face Palm} please set a digit in seconds for duration or don't set anything")
    else:
        duration = 5

    if duration > 360:
        return message.reply("\N{Face Palm} duraction too long")

    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        await message.reply_video(await camera.capture_video(duration))
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture video ({ex})")
    finally:
        await notification_message.delete()
