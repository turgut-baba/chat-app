from abc import ABC, abstractmethod
from typing import Callable

class Producer(ABC):

    @abstractmethod
    async def send_message(self, message, queue_name):
        pass
