import logging
import asyncio
import aiohttp
import json

from typing import List
from aiogram.types import Message, BotCommand

from app.config import config
from app.misc.command_description import CommandDescription
from app.misc.moonraker_service import MoonrakerService

logger = logging.getLogger(__name__)

moonraker = MoonrakerService(config.moonraker.url)
session = aiohttp.ClientSession()

async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def cmd_status(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        photo = await download(config.jpeg_stream.url)

        data = await moonraker.request("printer.objects.query", {
            "objects": {
                "print_stats": None,
                "display_status": None,
                "heater_bed": None,
                "extruder": None
            }
        })

        state = data["status"]["print_stats"]["state"]
        extruder_temperature = data["status"]["extruder"]["temperature"]
        extruder_target = data["status"]["extruder"]["target"]
        bed_temperature = data["status"]["heater_bed"]["temperature"]
        bed_target = data["status"]["heater_bed"]["target"]
        filename = data["status"]["print_stats"]["filename"]
        progress = data["status"]["display_status"]["progress"]

        caption = \
            f"\N{Weary Cat Face} " f"<code>{state}</code>\n"

        if int(extruder_temperature) > 0:
            caption += \
                f"\N{Thermometer} "    f"<code>extruder: {extruder_temperature} ({extruder_target})</code>\n" \

        if int(bed_temperature) > 0:
            caption += \
                f"\N{Thermometer} "    f"<code>bed: {bed_temperature} ({bed_target})</code>\n" \

        if state == "printing":
            caption += \
                f"\N{Memo} "           f"<code>file: {filename}</code>\n" \
                f"\N{Chequered Flag} " f"<code>progress: {int(progress * 100)}%</code>\n"

        await message.reply_photo(photo, caption=caption)

    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
        logger.exception(f"exception during process message {message}")
    finally:
        await notification_message.delete()

def register_main_group_status(storage: List[CommandDescription]):
    # Start moonraker service
    asyncio.ensure_future(moonraker.run())

    storage.append(
        CommandDescription(
            command = "status",
            description = "get printer status",
            func = cmd_status
        )
    )
