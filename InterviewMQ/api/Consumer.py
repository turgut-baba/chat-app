from abc import ABC, abstractmethod
from typing import Callable
from InterviewMQ.util.status import Status

class Consumer(ABC):

    @abstractmethod
    async def on_message(self, message):
        pass

    @abstractmethod
    async def listen_for_messages(self, queue_name):
        pass

    @abstractmethod 
    async def subscribe(self, queue_name: str, callback: Callable):
        pass

    @abstractmethod
    def start_consuming(self, queue_name):
        pass

    @abstractmethod
    async def filter_messages(self, message: dict, criteria: dict) -> bool:
        pass

    @abstractmethod
    async def send_to_websockets(self, message: dict):
        pass
