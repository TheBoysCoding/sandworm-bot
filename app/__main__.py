import logging
import asyncio

from aiogram.types import ParseMode, Message, BotCommand
from aiogram import Bot, Dispatcher

from app.config import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

from app.handlers.main_group_start import register_main_group_start
from app.handlers.main_group_mjpeg_stream import register_main_group_mjpeg_stream

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
            logger.exception(f"failed to send message to chat_id={chat_id}")

async def main() -> None:
    logger.info(f"config:\n{config}")

    bot = Bot(token=config.telegram.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot)

    commands = []

    # register commands
    register_main_group_mjpeg_stream(commands)
    register_main_group_start(commands)

    # make commands available for bot
    for command in commands:
        dp.register_message_handler(command.func, commands=command.command, chat_id=config.telegram.chats)

    # set /-commands in ui
    await bot.set_my_commands(
        [BotCommand(command=command.command, description=command.description) for command in commands]
    )

    logger.info("starting bot")

    # skip pending updates
    await dp.skip_updates()

    # send greeting
    await send_greeting(dp.bot)

    # start polling
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        logger.info("done")

if __name__ == '__main__':
    try:
        asyncio.run(main())
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(asyncio.gather(*[main(), moonraker.run()]))
    except (KeyboardInterrupt, SystemExit):
        logger.error("bot stopped!")
