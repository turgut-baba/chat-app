from queue import Queue
from typing import Callable
from pydantic import BaseModel
from util.status import Status
from fastapi import WebSocket
from typing import List
import asyncio
from typing import Dict
from collections import defaultdict

class Message(BaseModel):
    topic: str
    msg: str | None = None
    sent: bool = False
    in_queue: bool = True

class ConnectionManager:
    def __init__(self):
        self.websocket_connections = defaultdict(lambda: [])
        self.sse_queues: List[asyncio.Queue] = []

    async def add_sse_connection(self, queue: asyncio.Queue):
        self.sse_queues.append(queue)

    async def remove_sse_connection(self, queue: asyncio.Queue):
        self.sse_queues.remove(queue)

    async def add_websocket_connection(self, topic: str, websocket: WebSocket):
        self.websocket_connections[topic].append(websocket)

    async def remove_websocket_connection(self, topic:str, websocket: WebSocket):
        self.websocket_connections[topic].remove(websocket)

    async def broadcast(self, topic: str, message: str):
        # Send message to WebSocket clients
        for websocket in self.websocket_connections[topic]:
            try:
                await websocket.send_text(message)
            except Exception:
                await self.remove_websocket_connection(websocket)

        # Send message to SSE clients
        for queue in self.sse_queues:
            await queue.put(message)