__version__ = '1.0.0'
__author__ = 'Turgut Bababalım'
__contact__ = 'turgutbababalim@gmail.com'
__homepage__ = 'https://github.com/turgut-baba/chat-app'
__keywords__ = 'Asynchronous Message Queue Abstraction Library'

from fastapi import FastAPI
from InterviewMQ.system.websocket import router

app = FastAPI()

app.include_router(router)
    
print("TestAAAA")