import logging
import aiohttp

from app.config import config

logger = logging.getLogger(__name__)

class Moonraker:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def run(self):
        ws = await self.session.ws_connect(config.moonraker.url)
        while True:
            msg = await ws.receive()
            logger.info(f"data: {msg.data}")


moonraker = Moonraker()
