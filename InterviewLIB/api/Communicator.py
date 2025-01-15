from .Settings import ConnectionMethod
from typing import Callable, Union
import asyncio
from abc import abstractmethod

class Communicator:

    def __init__(self, url):
        self._method = ConnectionMethod.WS
        self._url = url
        self._websocket = None
        self._has_filter = False
        self._retries = 3

    def set_filter(self, filter: Union[str, Callable]):

        """ Can either set custom filter function or a simple string to filter for."""

        self.filter = filter
        self._has_filter = True

    def set_retries(self, retries: int) -> None:
        self._retries = retries

    async def _retry(self, func: Callable, *args, **kwargs):
        for attempt in range(1, self._retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                weight = 0.5
                wait_time = weight * (2 ** (attempt - 1))
                print(f"Attempt {attempt} failed: {e}. Retrying in {wait_time:.2f}s...")
                await asyncio.sleep(wait_time)

        print("Retry limit reached. Giving up.")
        raise Exception(f"Failed to process message after {self._retries} retries.")


    async def restart_service(self, seconds: int = 3) -> None:
        print("Restarting service...")
        await asyncio.sleep(seconds)
        print("Service restarted successfully.")

    def check_filter(self, message: str):
        if isinstance(self.filter, str):
            return self.filter in message
        elif isinstance(self.filter, Callable):
            return self.filter(message)

    def set_connection(self, Connection):
        self._method = Connection

    async def run(self, *topic):
        """Start the WebSocket client."""
        if(self._method == ConnectionMethod.WS):
            return await self._retry(self.run_ws, *topic)
        elif (self._method == ConnectionMethod.HTTP):
            return await self._retry(self.run_http, *topic)

    @abstractmethod
    def run_ws(self):
        ...

    @abstractmethod
    def run_http(self):
        ...