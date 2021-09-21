import logging
import asyncio

from aiogram.types import BotCommand, ParseMode
from aiogram import Bot, Dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

log = logging.getLogger(__name__)

from app.handlers.commands import register_commands
from app.config import config
from app.core import commands

def get_notify_chats():
    yield from config.telegram.chats

async def notify_message(dp: Dispatcher, text: str):
    for chat_id in get_notify_chats():
        try:
            await dp.bot.send_message(chat_id, text)
        except:
            log.exception(f"failed to send message to chat_id={chat_id}")

async def notify_sticker(dp: Dispatcher, sticker_id: str):
    for chat_id in get_notify_chats():
        try:
            await dp.bot.send_sticker(chat_id, sticker_id)
        except:
            log.exception(f"failed to send sticker to chat_id={chat_id}")

async def start_telegram_bot(dp: Dispatcher) -> None:
    log.info("starting telegram bot")

    await dp.skip_updates()

    await dp.bot.set_my_commands(
        [BotCommand(command=command, description=description) for command, description in commands]
    )

    greeting_sticker = config.stickers.get("greeting", None)
    if greeting_sticker is None:
        await notify_message(dp, "\N{Robot Face} bot online")
    else:
        await notify_sticker(dp, greeting_sticker)

    await dp.start_polling()

def main() -> None:
    log.info(f"config:\n{config}")

    loop = asyncio.get_event_loop()

    bot = Bot(token=config.telegram.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot)

    register_commands(dp, chat_id=config.telegram.chats)

    try:
        asyncio.ensure_future(start_telegram_bot(dp))
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("CTRL-C")
    finally:
        log.info("done")

if __name__ == '__main__':
    main()
