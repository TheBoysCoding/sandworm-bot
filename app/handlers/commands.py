import asyncio

from aiogram import Dispatcher
from aiogram.types import Message

from app.config import config
from app.misc import Camera
from app.core import commands

camera = Camera(device=config.camera.device)

async def command_start(message: Message):
    help_message = "".join(f"{command} - {description}\n" for command, description in commands)

    await message.answer(help_message)

async def command_photo(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        await message.reply_photo(await camera.capture_photo())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
    finally:
        await notification_message.delete()

async def command_video(message: Message):
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

def register_commands(dp: Dispatcher, **kwargs):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(command_photo, commands="photo")
    dp.register_message_handler(command_video, commands="video")

