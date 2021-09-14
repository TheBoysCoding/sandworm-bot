import asyncio
import logging

from aiogram.types import Message

from app import dp, config

log = logging.getLogger(__name__)
camera_lock = asyncio.Lock()

VIDEO_CAPTURE_DURATION = 5

async def run_ffmpeg(args: str):
    if config.camera.device is None:
        raise RuntimeError("camera not configure")

    if camera_lock.locked():
        raise RuntimeError("camera busy")

    async with camera_lock:
        cmd = f"ffmpeg -i {config.camera.device} {args} -"

        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            log.error(f"ffmpeg spawn error ({cmd})")
            raise RuntimeError(f"capture process return error {process.returncode}")

        return stdout

async def ffmpeg_capture_photo():
    return await run_ffmpeg("-frames:v 1 -f webp")

@dp.message_handler(commands="photo", chat_id=config.telegram.chats)
async def command_handler_photo(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        await message.reply_photo(await ffmpeg_capture_photo())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture photo ({ex})")
    finally:
        await notification_message.delete()

async def ffmpeg_capture_video():
    return await run_ffmpeg(f"-t {VIDEO_CAPTURE_DURATION} -an -c:v libx264 -crf 26 -vf scale=640:-1 -movflags frag_keyframe+empty_moov -f mp4 -pix_fmt yuv420p")

@dp.message_handler(commands="video", chat_id=config.telegram.chats)
async def command_handler_video(message: Message):
    notification_message = await message.answer("\N{SLEEPING SYMBOL}...")
    try:
        await message.reply_video(await ffmpeg_capture_video())
    except Exception as ex:
        await message.reply(f"\N{Heavy Ballot X} failed to capture video ({ex})")
    finally:
        await notification_message.delete()
