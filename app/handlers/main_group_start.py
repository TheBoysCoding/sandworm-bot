import asyncio

from aiogram import Dispatcher, Bot
from aiogram.types import Message, BotCommand

from app.config import config

bot_commands = (
    ('/help',   'Print this help'),
    ('/photo',  'Capture and send photo'),
    ('/video',  'Capture and send video'),
)

async def cmd_help(message: Message):
    help_message = "".join(f"{command} - {description}\n" for command, description in bot_commands)
    await message.answer(help_message)

def register_main_group_start(dp: Dispatcher):
    dp.register_message_handler(cmd_help, commands=["start", "help"], chat_id=config.telegram.chats)

async def register_bot_commands(bot: Bot):
    await bot.set_my_commands(
        [BotCommand(command=command, description=description) for command, description in bot_commands]
    )
