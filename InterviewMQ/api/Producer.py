""" from abc import ABC, abstractmethod
from typing import Callable
from InterviewMQ.util.status import Status

class Producer(ABC):

    @abstractmethod
    async def send_message(self, message, queue_name):
        pass

    @abstractmethod
    def publish(self, message, queue_name):
        pass

 """

import asyncio
import websockets

async def websocket_client():
    uri = "ws://localhost:8000/interviewmq"
    try:
        async with websockets.connect(uri) as websocket:
            # Send a message to the server
            await websocket.send("Hello from the WebSocket client!")
            print("Message sent to server.")
            
            # Receive a response from the server
            response = await websocket.recv()
            print(f"Server response: {response}")
    except Exception as e:
        print(f"WebSocket connection failed: {e}")

# Run the client
asyncio.run(websocket_client())
