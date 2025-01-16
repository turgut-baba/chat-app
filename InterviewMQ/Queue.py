from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from typing import List
from InterviewMQ.system.message import ConnectionManager
from collections import defaultdict

topics = defaultdict(lambda: [])

connected_clients = ConnectionManager()

router = APIRouter()

import InterviewMQ.system.websocket 
import InterviewMQ.system.restful 

