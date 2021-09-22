import logging
import asyncio

from aiogram.types import ParseMode, Message
from aiogram import Bot, Dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

log = logging.getLogger(__name__)

from app.handlers.main_group_start import register_main_group_start, register_bot_commands
from app.handlers.main_group_camera import register_main_group_camera
from app.config import config

def get_notify_chats():
    yield from config.telegram.chats

async def send_greeting(bot: Bot) -> None:
    sticker_id = config.stickers.get("greeting", None)

    for chat_id in get_notify_chats():
        try:
            if sticker_id is not None:
                await bot.send_sticker(chat_id, sticker_id)
            else:
                await bot.send_message(chat_id, text)
        except:
            log.exception(f"failed to send message to chat_id={chat_id}")

async def start_telegram_bot(dp: Dispatcher) -> None:
    log.info("starting telegram bot")

    register_main_group_start(dp)
    register_main_group_camera(dp)

    await register_bot_commands(dp.bot)

    await dp.skip_updates()
    await send_greeting(dp.bot)
    await dp.start_polling()

def main() -> None:
    log.info(f"config:\n{config}")

    loop = asyncio.get_event_loop()

    bot = Bot(token=config.telegram.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot)

    try:
        asyncio.ensure_future(start_telegram_bot(dp))
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("CTRL-C")
    finally:
        log.info("done")

if __name__ == '__main__':
    main()
