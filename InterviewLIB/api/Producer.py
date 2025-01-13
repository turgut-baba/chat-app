import asyncio
import websockets
import json
import requests
import httpx
from typing import Callable, Union
from .Communicator import Communicator

class Producer(Communicator):
    def __init__(self, uri):
        super().__init__(uri)

    async def publish(self, topic, message):
        await self.run(topic, message)

    async def run_ws(self, topic, message):
        message = {
                "command": "publish",
                "topic": topic,
                "msg": message
            }
        try:
            async with websockets.connect(self.url) as websocket:
                if not self.has_filter:
                    await websocket.send(json.dumps(message))
                    print("Message sent to server.")
                elif self.check_filter(message['msg']):
                    await websocket.send(json.dumps(message))
                    print("Message sent to server.")
                else:
                    print('Message does not fit filter criterias.')
                
                response = await websocket.recv()
                print(f"Server response: {response}")
                return response
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
        
    async def run_http(url, topic, message):
        payload = {
            "topic": topic,
            "msg": message
        }
        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Network response was not ok: {response.status_code}, {response.text}")

            return response.json()
