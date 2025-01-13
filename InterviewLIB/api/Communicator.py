from .Settings import ConnectionMethod
from typing import Callable, Union
import asyncio
from abc import abstractmethod

class Communicator:

    def __init__(self, url):
        self.method = ConnectionMethod.WS
        self.url = url
        self.websocket = None
        self.has_filter = False

    def set_filter(self, filter: Union[str, Callable]):
        self.filter = filter
        self.has_filter = True

    def check_filter(self, message: str):
        if isinstance(self.filter, str):
            return self.filter in message
        elif isinstance(self.filter, Callable):
            return self.filter()

    def set_connection(self, Connection):
        self.method = Connection

    async def run(self, *topic):
        """Start the WebSocket client."""
        if(self.method == ConnectionMethod.WS):
            await self.run_ws(*topic)
        elif (self.method == ConnectionMethod.HTTP):
            await self.run_http(*topic)

    @abstractmethod
    def run_ws(self):
        ...

    @abstractmethod
    def run_http(self):
        ...