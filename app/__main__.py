import logging
import asyncio

from aiogram.types import BotCommand

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

log = logging.getLogger(__name__)

from app import bot, dp, config, handlers, commands, notify_message, notify_sticker

async def send_greeting():
    greeting_sticker = config.stickers.get('greeting', None)

    for chat_id in get_notify_chats():
        if sticker is not None:
            await bot.send_sticker(chat_id, sticker=greeting_sticker)
        else:
            await bot.send_message(chat_id, "\N{Robot Face} bot online")

async def start_telegram_bot() -> None:
    log.info("starting telegram bot")

    await dp.skip_updates()

    await bot.set_my_commands(
        [BotCommand(command=command, description=description) for command, description in commands]
    )

    greeting_sticker = config.stickers.get("greeting", None)
    if greeting_sticker is None:
        await notify_message("\N{Robot Face} bot online")
    else:
        await notify_sticker(greeting_sticker)

    await dp.start_polling()

def main() -> None:
    log.info(f"config:\n{config}")

    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(start_telegram_bot())
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("CTRL-C")
    finally:
        log.info("done")

if __name__ == '__main__':
    main()
