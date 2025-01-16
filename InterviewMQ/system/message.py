from queue import Queue
from typing import Callable
from pydantic import BaseModel
from InterviewMQ.util.status import Status
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
        self.sse_queues = defaultdict(lambda: [])

    async def add_sse_connection(self, topic: str, queue: asyncio.Queue):
        self.sse_queues[topic].append(queue)

    async def remove_sse_connection(self, topic: str, queue: asyncio.Queue):
        self.sse_queues[topic].remove(queue)

    async def add_websocket_connection(self, topic: str, websocket: WebSocket):
        self.websocket_connections[topic].append(websocket)

    async def remove_websocket_connection(self, topic:str, websocket: WebSocket):
        self.websocket_connections[topic].remove(websocket)

    async def clear(self):
        self.websocket_connections.clear()
        self.sse_queues.clear()

    async def broadcast(self, topic: str, message: str):
        # Send message to WebSocket clients
        for websocket in self.websocket_connections[topic]:
            try:
                await websocket.send_text(message)
            except Exception:
                await self.remove_websocket_connection(topic, websocket)

        # Send message to SSE clients
        for queue in self.sse_queues[topic]:
            try:
                await queue.put(message)
            except Exception:
                await self.remove_sse_connection(topic, websocket)

            