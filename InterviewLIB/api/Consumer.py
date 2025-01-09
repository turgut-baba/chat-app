from abc import ABC, abstractmethod
from typing import Callable

class Consumer(ABC):

    @abstractmethod 
    async def subscribe(self, queue_name: str):
        pass

    @abstractmethod
    async def filter_messages(self, message: dict, criteria: dict) -> bool:
        pass

