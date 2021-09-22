import asyncio
import logging

class Camera:
    def __init__(self, *, device: str = None,  loop: asyncio.AbstractEventLoop = None):
        self._logger = logging.getLogger(__name__)
        self._device = device
        self._loop = loop or asyncio.get_event_loop()
        self._lock = asyncio.Lock()

    async def capture_photo(self):
        return await self._ffmpeg_run("-frames:v 1 -f webp")

    async def capture_video(self, duration: int):
        return await self._ffmpeg_run(f"-t {duration} -an -c:v libx264 -crf 26 -vf scale=640:-1 -movflags frag_keyframe+empty_moov -f mp4 -pix_fmt yuv420p")

    async def _ffmpeg_run(self, args: str):
        if self._device is None:
            raise RuntimeError("device not set")

        if self._lock.locked():
            raise RuntimeError("camera busy")

        async with self._lock:
            cmd = f"ffmpeg -i {self._device} {args} -"

            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                self._logger.error(f"ffmpeg spawn error ({cmd})")
                raise RuntimeError(f"capture process return error {process.returncode}")

            return stdout
