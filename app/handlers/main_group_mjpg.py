import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiohttp import ClientSession
from typing import List

from app.config import config
from app.misc.command_description import CommandDescription

logger = logging.getLogger(__name__)

async def cmd_mjpg_photo(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        async with ClientSession() as session:
            async with session.get(config.jpeg_stream.url) as response:
                await message.reply_photo(await response.read())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
        logger.exception(f"exception during process message {message}")
    finally:
        await notification_message.delete()

def register_main_group_mjpg(storage: List[CommandDescription]) -> None:
    storage.append(
        CommandDescription(
            command = "photo",
            description = "capture and send a photo",
            func = cmd_mjpg_photo
        )
    )
