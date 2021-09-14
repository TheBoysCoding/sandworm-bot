from aiogram.types import Message

from app import dp, config, commands

@dp.message_handler(commands=["start", "help"], chat_id=config.telegram.chats)
async def command_handler_start(message: Message):
    help_message = "".join(f"{command} - {description}\n" for command, description in commands)

    await message.answer(help_message)
