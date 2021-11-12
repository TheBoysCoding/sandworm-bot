from typing import List
from aiogram.types import Message, BotCommand

from app.misc.command_description import CommandDescription

def register_main_group_start(storage: List[CommandDescription]):
    async def cmd_help(message: Message):
        help_message = "".join(f"/{command.command} - {command.description}\n" for command in storage)
        await message.answer(help_message)

    storage.append(
        CommandDescription(
            command = "help",
            description = "print this help",
            func = cmd_help
        )
    )
