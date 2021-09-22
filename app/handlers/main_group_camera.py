import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import Message

from app.config import config
from app.misc.camera import Camera

log = logging.getLogger(__name__)
camera = Camera(device=config.camera.device)

async def cmd_photo(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        await message.reply_photo(await camera.capture_photo())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
        log.exception(f"exception during process message {message}")
    finally:
        await notification_message.delete()

async def cmd_video(message: Message):
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
        log.exception(f"exception during process message {message}")
    finally:
        await notification_message.delete()

def register_main_group_camera(dp: Dispatcher):
    dp.register_message_handler(cmd_photo, commands="photo", chat_id=config.telegram.chats)
    dp.register_message_handler(cmd_video, commands="video", chat_id=config.telegram.chats)

