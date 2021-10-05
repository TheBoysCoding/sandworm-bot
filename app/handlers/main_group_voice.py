import logging

from aiogram import Dispatcher
from aiogram.types import Message
from gtts import gTTS
from tempfile import TemporaryFile

from app.config import config

logger = logging.getLogger(__name__)

async def cmd_voice(message: Message):
    text = message.get_args()
    if not text:
        return await message.reply(f"\N{Heavy Ballot X} text not set")

    try:
        tts = gTTS(text=text, lang="ru")
        tmp = TemporaryFile()
        tts.write_to_fp(tmp)
        tmp.seek(0)
        await message.reply_voice(tmp.read())
    finally:
        tmp.close()

def register_main_group_voice(dp: Dispatcher):
    dp.register_message_handler(cmd_voice, commands="voice", chat_id=config.telegram.chats)
