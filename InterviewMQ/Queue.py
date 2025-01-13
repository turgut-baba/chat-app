from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from typing import List
from InterviewMQ.util.logger import Logger
from InterviewMQ.system.message import ConnectionManager
from collections import defaultdict

topics = defaultdict(lambda: [])
logger = Logger("server.log", "InterviewMQ")

# In-memory message queue
message_queue = asyncio.Queue()

# Store connected WebSocket clients
#connected_clients: List[WebSocket] = []

connected_clients = ConnectionManager()

router = APIRouter()

import InterviewMQ.system.websocket 
import InterviewMQ.system.restful 