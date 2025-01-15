from enum import Enum

class Status(Enum):
    SUCCESS = 100
    IDLE = 200
    WARNING = 300
    FAIL = 400
    CRITICAL = 500