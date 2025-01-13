__version__ = '1.0.0'
__author__ = 'Turgut Bababalım'
__contact__ = 'turgutbababalim@gmail.com'
__homepage__ = 'https://github.com/turgut-baba/chat-app'
__keywords__ = 'Asynchronous Message Queue Abstraction Library'

from fastapi import FastAPI
from InterviewMQ.Queue import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)