from enum import Enum

class Status(Enum):
    SUCCESS = 1
    IDLE = 2
    WARNING = 3
    FAIL = 4
    CRITICAL = 5