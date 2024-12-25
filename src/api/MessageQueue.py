from abc import ABC, abstractmethod
from typing import Callable
from src.util.status import Status

class MessageQueue(ABC):

    @abstractmethod
    async def queue_message(self, Process: Callable) -> Status:
        """Send a message to the specified topic."""
        pass

    @abstractmethod
    async def send_single_message(self, message)  -> Status:
        """Send a message to the specified topic."""
        pass

    @abstractmethod
    async def send_queued_messages(self, topic: str, message: dict)  -> Status:
        """Send a message to the specified topic."""
        pass

    @abstractmethod
    async def receive_message(self, topic: str) -> dict:
        """Receive a message from the specified topic."""
        pass

    @abstractmethod
    async def publish():
        pass

    @abstractmethod
    async def subscribe():
        pass

    @abstractmethod
    async def filter_message():
        pass