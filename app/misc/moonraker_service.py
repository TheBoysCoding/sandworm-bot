import asyncio
import aiohttp
import json
import logging

from typing import Optional, Callable, Any

class MoonrakerService:
    def __init__(self, url: str, loop=None):
        self._logger = logging.getLogger('MoonrakerService')
        self._url = url
        self._loop = loop
        self._session = None
        self._running = False
        self._websocket = None
        self._reconnect_timeout = 5.0
        self._next_connect_attempt = None
        self._next_request_id = 0
        self._pending_requests = dict()

    async def run(self) -> None:
        self._running = True

        try:
            while self._running:
                await self._wait_reconnect_time()

                try:
                    if self._session is None or self._session.closed:
                        self._session = aiohttp.ClientSession(loop=self._loop)
                    self._logger.info(f'connecting to {self._url}')
                    self._websocket = await self._session.ws_connect(self._url)
                    self._logger.info('connection established')
                except Exception as e:
                    self._logger.warning(f'connection error: {e}')
                    continue

                # clear before send any message
                self._pending_requests.clear()

                while self._websocket and not self._websocket.closed:
                    message = await self._websocket.receive()

                    if message.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR):
                        continue

                    if message.type == aiohttp.WSMsgType.TEXT:
                        try:
                            await self._handle_message(message.json())
                        except ValueError as ex:
                            self._logger.error(f'failed to parse json \"{message.data}\"')
        finally:
            await self._websocket.close()
            await self._session.close()


    async def shutdown(self) -> None:
        self._running = False
        if self._websocket:
            await self._websocket.close()
        if self._session:
            await self._session.close()

    async def _wait_reconnect_time(self) -> None:
        loop = asyncio.get_running_loop()
        if self._next_connect_attempt is None:
            self._next_connect_attempt = loop.time()
        if self._next_connect_attempt > loop.time():
            await asyncio.sleep(self._next_connect_attempt - loop.time())
        self._next_connect_attempt = loop.time() + self._reconnect_timeout

    async def request(self, method, params: Optional[Any] = None):
        if self._websocket is None or self._websocket.closed:
            raise RuntimeError('not connected')

        # request id
        request_id = self._next_request_id

        self._next_request_id += 1

        # prepare request
        request = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': request_id
        }

        future = asyncio.get_running_loop().create_future()

        # store callback
        self._pending_requests[request_id] = future

        # send message
        await self._websocket.send_str(json.dumps(request))

        # wait result
        await future

        if future.exception():
            raise future.exception()

        result = future.result()
        if 'error' in result:
            raise RuntimeError(result['error']['message'])

        return result['result']

    async def _handle_message(self, data) -> None:
        # self._logger.info(f'_xxx: {data}')

        if 'method' in data:
            method = data['method']

            if method == 'notify_proc_stat_update':
                pass
            elif method == 'notify_status_update':
                pass

            #params = data['params']
            #self._logger.info(f'{data}')
        else:
            request_id = data['id']
            if request_id in self._pending_requests:
                future = self._pending_requests[request_id]
                future.set_result(data)
                del self._pending_requests[request_id]
