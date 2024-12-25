from queue import Queue
from typing import Callable

from util.status import Status

class Message:

    # TODO: think about how message will be handled, str or callable.
    def __init__(self, message: str):
        self.handled = False
        self.in_queue = False
        self.executing = False

        self.message = message

    def set_in_quee(self, switch: bool) -> None:
        self.in_queue = switch

    def add_process(self, process: Callable) -> Status:
        self.process = process

    def _run(self) -> None:
        self.process()